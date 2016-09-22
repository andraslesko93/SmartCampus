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
