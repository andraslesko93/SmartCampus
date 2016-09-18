function getCurrentDate (offsetInHour) {
	  var now = new Date($.now())
	    , year
	    , month
	    , date
	    , hours
	    , minutes
	    , seconds
	    , formattedDateTime
	    ;
	  
	  year = now.getFullYear();
	  month = now.getMonth().toString().length === 1 ? '0' + (now.getMonth() + 1).toString() : now.getMonth() + 1;
	  date = now.getDate().toString().length === 1 ? '0' + (now.getDate()).toString() : now.getDate();
	  hours = now.getHours().toString().length === 1 ? '0' + now.getHours().toString() : now.getHours();
	  minutes = now.getMinutes().toString().length === 1 ? '0' + now.getMinutes().toString() : now.getMinutes();
	  seconds = now.getSeconds().toString().length === 1 ? '0' + now.getSeconds().toString() : now.getSeconds();
	  
	  hours=hours+offsetInHour;
	  formattedDateTime = year + '-' + month + '-' + date + 'T' + hours + ':' + minutes + ':' + seconds;

	  return formattedDateTime;
}


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
