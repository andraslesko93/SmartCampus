$( document ).ready( function() {
	$('textarea').each(function() {
		
	    var id = $( this ).attr("id");
	    var left = $( this ).attr("maxlength") - $( this ).val().length;
	    var textAreaCounter= $("#"+id+"Counter");
	    textAreaCounter.html($('<small>You have '+left+' characters left.</small>'));
	});	
    $( this ).find( "textarea" ).on( "input change propertychange", function() {
    	var left = $( this ).attr( "maxlength") - $(this).val().length;
        if (left < 0) {
            left = 0;           
        }
        var id = $( this ).attr("id");
        var textAreaCounter= $("#"+id+"Counter");
        textAreaCounter.html($('<small>You have '+left+' characters left.</small>'));
    });
});