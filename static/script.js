var $animateSet = $("#top-background, #loading-indicator, #logo-image, #search-bar");

$("#search-button").on("click", function() {
  var query = $("#queryField").val();
  $("#loading-indicator").removeClass("ready");
  $animateSet.addClass("go-top");
  searchQuery(query)
  processResults();
});

$("#search-bar").find("input").on('keyup', function(e) {
  if (e.keyCode == 13) {
    $("#search-results").removeClass("show");
    $("#search-button").trigger('click');
  }
});

function searchQuery(query) {
  $.ajax({
    url: 'http://tanya-dokter.herokuapp.com/api/search/?q1='+query,
    method: 'GET',
    contentType: 'application/json',
    error: function() {
      $('#search-results').html('<p>An error has occurred</p>');
    },
    success: function(resp) {
      for (i = 1; i <= 10; i++) { 
        var $entry = '<li class="list-group-item"><a href="#">'+ resp[i].disease +'</a></li>';
        $('#search-results').append($entry);
      }
    },
  });
}

var indicatorTimeout;
function processResults() {
  $('#search-results').html("");
  clearTimeout(indicatorTimeout);
  indicatorTimeout = setTimeout(function() {
    $("#loading-indicator").removeClass("go-top").addClass("ready");
    
  }, 1250);

  showResults();
}

var $searchResults = $("#search-results");
var resultsInterval;
function showResults() {
  $searchResults.addClass("show");
  var $results = $searchResults.children();
  var count = $results.length;
  
  clearInterval(resultsInterval);
  
  var i = 0;
  resultsInterval = setInterval(function() {
    if (i < count) {
      $($results[i]).addClass("show");
      i++;
    } else {
      clearInterval(resultsInterval);
    }
  }, 150);
}
