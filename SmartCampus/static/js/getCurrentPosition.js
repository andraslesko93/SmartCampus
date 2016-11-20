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
