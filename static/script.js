var $animateSet = $("#top-background, #loading-indicator, #logo-image, #search-bar");

$("#search-button").on("click", function() {
  $("#loading-indicator").removeClass("ready");
  $animateSet.addClass("go-top");
  console.log("hai");
  processResults();
});

$("#search-bar").find("input").on('keyup', function(e) {
  if (e.keyCode == 13) {
  $("#search-results").removeClass("show");
  $("#search-button").trigger('click');
    }
});

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