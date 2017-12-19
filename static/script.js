var $animateSet = $("#top-background, #loading-indicator, #logo-image, #search-bar");

$("#search-button").on("click", function() {
  var query = $("#queryField").val();
  $("#loading-indicator").removeClass("ready");
  $animateSet.addClass("go-top");
  $("#search-results").html("")
  searchQuery(query)
});

$("#search-bar").find("input").on('keyup', function(e) {
  if (e.keyCode == 13) {
    var query = $("#queryField").val();
    $("#search-results").removeClass("show");
    $("#search-button").trigger('click');
  }
});

function searchQuery(query) {
  $.ajax({
   url: 'http://localhost:5000/api/search/?q1='+query,
   method: 'GET',
   contentType: 'application/json',
   crossDomain:true,
   error: function() {
      $('#search-results').html('<p>An error has occurred</p>');
   },
   success: function(resp) {
      console.log(resp)
      for (i = 1; i <= 10; i++) { 
        var $entry = '<li class="list-group-item"><a href="#">'+ resp[i].disease +'</a></li>';
        $('#search-results')
         .append($entry);
      }
      
      processResults();
   },
});
}

var indicatorTimeout;
function processResults() {
  clearTimeout(indicatorTimeout);
  indicatorTimeout = setTimeout(function() {
    $("#loading-indicator").removeClass("go-top").addClass("ready");
    
    showResults();
  }, 1250);
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