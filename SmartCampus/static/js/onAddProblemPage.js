$('#classisProblemFormDateTime').on( "input change propertychange", function(){
	
	var givenDate = $(this).val();
    if (givenDate < getCurrentDate(0))
    {
        this.setCustomValidity("You can't create a problem in the past.");
    } 
    else if(givenDate < getCurrentDate(1))
    {        
    	this.setCustomValidity("You can't create a problem with such a close deadline. There should be at least 1 hour until its deadline passes.");
    }
    else 
    {
        this.setCustomValidity('');
    }
});

$('#confProblemFormDateTime').on( "input change propertychange", function(){
	
	var givenDate = $(this).val();
    if (givenDate < getCurrentDate(0))
    {
        this.setCustomValidity("You can't create a problem in the past.");
    } 
    else if(givenDate < getCurrentDate(1))
    {        
    	this.setCustomValidity("You can't create a problem with such a close deadline. There should be at least 1 hour until its deadline passes.");
    }
    else 
    {
        this.setCustomValidity('');
    }
});

if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
	$('#canvas-column').hide();
}

var myOptions = {
   	mapTypeId: google.maps.MapTypeId.ROADMAP,
   	mapTypeControl: false
   };
var map = new google.maps.Map(document.getElementById("map_canvas"),myOptions);
var infoWindow = new google.maps.InfoWindow();
var bounds = new google.maps.LatLngBounds();
map.fitBounds(bounds);
var infoWindow = new google.maps.InfoWindow({map: map});

if (navigator.geolocation) {
       navigator.geolocation.getCurrentPosition(function(position) {
         var pos = {
           lat: position.coords.latitude,
           lng: position.coords.longitude
         };
         infoWindow.setPosition(pos);
         infoWindow.setContent('You are here.');
     map.setCenter(pos);
   }, function() {
     handleLocationError(true, infoWindow, map.getCenter());
   });
}
else {
   // Browser doesn't support Geolocation
       handleLocationError(false, infoWindow, map.getCenter());
}
var classicProblemInput = document.getElementById('classicProblemLocation');
var confidenceProblemInput = document.getElementById('confidenceProblemLocation');
var options = {
    componentRestrictions: {country: 'hu'}
};

var marker=new google.maps.Marker();

var classicProblemAutocomplete = new google.maps.places.Autocomplete(classicProblemInput, options);
google.maps.event.addListener(classicProblemAutocomplete, 'place_changed', function () {
	var place = classicProblemAutocomplete.getPlace();
    var markerCoords= [place.name, place.geometry.location.lat(),place.geometry.location.lng()];
    $('#classicProblemLat').val(place.geometry.location.lat());
    $('#classicProblemLng').val(place.geometry.location.lng());
    drawAMarker(markerCoords);
});

if(confidenceProblemInput != null){
	var confidenceProblemAutocomplete = new google.maps.places.Autocomplete(confidenceProblemInput, options);
	google.maps.event.addListener(confidenceProblemAutocomplete, 'place_changed', function () {
		var place = confidenceProblemAutocomplete.getPlace();
	    var markerCoords= [place.name, place.geometry.location.lat(),place.geometry.location.lng()];  
	    $('#confidenceProblemLat').val(place.geometry.location.lat());
	    $('#confidenceProblemLng').val(place.geometry.location.lng());
	    drawAMarker(markerCoords);
	});
}


google.maps.Map.prototype.clearMarkers = function() {
    for(var i=0; i < this.markers.length; i++){
        this.markers[i].setMap(null);
    }
    this.markers = new Array();
};
function drawAMarker(inputMarkerCoords)
{

	marker.setMap(null);
   	var pos = new google.maps.LatLng(inputMarkerCoords[1], inputMarkerCoords[2]);
   	var bounds = new google.maps.LatLngBounds();
    bounds.extend(pos);
   	marker = new google.maps.Marker({
   		position: pos,
   		map: map
   	});
   	google.maps.event.addListener(marker, 'click', (function(marker) {
   		return function() {
   			infoWindow.setContent(inputMarkerCoords[0]);
   			infoWindow.open(map, marker);
   		}
   	})(marker));
   	
   	map = marker.getMap();  
   	map.setCenter(pos); // set map center to marker position
    smoothZoom(map, 12, map.getZoom());
    map.fitBounds(bounds);

}


function getCurrentPosition() {
    var deferred = $.Deferred();
    // if geo location is supported
    if(navigator.geolocation) {
        // get current position and pass the results to getPostalCode or time out after 5 seconds if it fails
        navigator.geolocation.getCurrentPosition(deferred.resolve, geoLocationError, {
            timeout: 5000
        });
    } else {
        //geo location isn't supported
        console.log('Your browser does not support Geo Location.');
    }
    return deferred.promise();
}
		    
function geoLocationError() {
    console.log('Geo Location failed.');
}

function smoothZoom (map, max, cnt) {
    if (cnt >= max) {
        return;
    }
    else {
        z = google.maps.event.addListener(map, 'zoom_changed', function(event){
            google.maps.event.removeListener(z);
            smoothZoom(map, max, cnt + 1);
        });
        setTimeout(function(){map.setZoom(cnt)}, 80); // 80ms is what I found to work well on my system -- it might not work well on all systems
    }
}