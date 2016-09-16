$( document ).ready( function() {
    var errorMessage = "Please match the requested format.";

    $( this ).find( "textarea" ).on( "input change propertychange", function() {

        var pattern = $( this ).attr( "pattern" );

        if(typeof pattern !== typeof undefined && pattern !== false)
        {
            var patternRegex = new RegExp( "^" + pattern.replace(/^\^|\$$/g, '') + "$", "g" );

            hasError = !$( this ).val().match( patternRegex );

            if ( typeof this.setCustomValidity === "function") 
            {
            	var titleText= $( this ).attr( "title");
            	errorMessageWithTitle = errorMessage+" "+titleText;
                this.setCustomValidity( hasError ? errorMessageWithTitle: "");
                errorMessageWithTitle=errorMessage;
            } 
            else 
            {
                $( this ).toggleClass( "error", !!hasError );
                $( this ).toggleClass( "ok", !hasError );;
                if ( hasError ) 
                {
                    $( this ).attr( "title", errorMessage);
                } 
                else
                {
                    $( this ).removeAttr( "title" );
                }
            }
        }

    });
});