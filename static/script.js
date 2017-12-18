var $animateSet = $("#top-background, #loading-indicator, #logo-image, #search-bar");

$("#search-button").on("click", function() {
  var query = $("#queryField").val();
  $("#loading-indicator").removeClass("ready");
  $animateSet.addClass("go-top");
  console.log(query)
  searchQuery(query )
  console.log("hai");
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
   error: function() {
      $('#info').html('<p>An error has occurred</p>');
   },
   success: function(data) {
      console.log(data)
      for (i = 0; i < 10; i++) { 
        var $title = $('<h1>').text(data.disease[i]);
        var $description = $('<p>').text(data.raw_data[i]);
        $('#info')
         .append($title)
         .append($description);
      }

   },
     type: 'GET'
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