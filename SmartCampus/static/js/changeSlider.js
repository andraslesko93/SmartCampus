function changeSlider(id) {
    var range = document.getElementById(id).value;
    var rangeWindow = $("#"+id+"Window");

    if (range==1)
    {
    	rangeWindow.empty();
    	$('<i class="fa fa-frown-o" aria-hidden="true"></i>').appendTo(rangeWindow);
    }	
    
    else if(range==2)	
    {
    	rangeWindow.empty();
    	$('<i class="fa fa-meh-o" aria-hidden="true"></i>').appendTo(rangeWindow);
    }
    else if (range==3)
    {
    	rangeWindow.empty();
    	$('<i class="fa fa-smile-o" aria-hidden="true"></i>').appendTo(rangeWindow);
    }
}