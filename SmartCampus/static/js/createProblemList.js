function createProblemList (appendElementId, jsonLink)
{	
	$.when(getCurrentPosition()).then(function(data, textStatus, jqXHR) {
		//console.log(data.coords.longitude, data.coords.latitude);
		//console.log(jsonLink);
		$.ajax({
			type: 'GET',
		    url: jsonLink,
		    dataType: "json",
		    data: {'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value, 
		    	'lat':data.coords.latitude,
		    	'lng':data.coords.longitude,
		    	},
		    success: function (data) {
		    	appendElement = $('<div id='+appendElementId+'></div>');
		    	if(data.length==0)
	    			{
	    				$('#'+appendElementId+'').replaceWith(appendElement);
	    			return;
	    			}
	    		var col = $('<div class ="col-xs-12 col-md-6">').appendTo(appendElement);
	    		$.each(data, function(i, obj) 
	    		{	
	    			/*console.log("user: "+obj.user+
	    	                " picture: "+obj.picture+
	    	                " user_link: "+obj.user_link+
	    	                " title: "+obj.title+
	    	                " problem_link"+obj.problem_link+
	    	                " description: "+obj.description+
	    	                " deadline: "+obj.deadline+
	    	                " tags: "+obj.tags+
	    	                " bounty: "+obj.bounty+
	    	                " min_rq_repu: "+obj.minimum_required_reputation
	    	                );*/
	    			var row = $('<div class ="row">').appendTo(col);
	    			var innerCol = $('<div class="col-xs-12">').appendTo(row);
	    			var roundBox = $('<div class="round-box">').appendTo(innerCol);
	    			
	    			
	    			var titleRow = $('<div class = "row">').appendTo(roundBox);
	    			var pictureCol =$('<div class ="col-xs-1">').appendTo(titleRow);
	    			$('<a href='+String(obj.user_link)+' id="user-link-element"> <img src="'+String(obj.picture)+'" width="50"/> </a>').appendTo(pictureCol);
	    			var nameAndLinkCol = $('<div class ="col-xs-9 col-md-9 col-lg-9">').appendTo(titleRow);
	    			var nameAndLinkContainer = $('<div class ="name-and-link-container">').appendTo(nameAndLinkCol);
	    			var nameAndLinkParagraph = $('<p>').appendTo(nameAndLinkContainer);
	    			
	    			$('<a href="'+String(obj.problem_link)+'" id="problem-link-element"><strong>'+String(obj.title)+'</strong></a>').appendTo(nameAndLinkParagraph);
	    			$('<br/>').appendTo(nameAndLinkParagraph);
	    			
	    			$('<i><small>by: <strong><a href='+String(obj.user_link)+' id="user-link-element">'+String(obj.user)+'</a><strong></i></small>').appendTo(nameAndLinkParagraph);
	    			var problemLink = $('<a href="'+String(obj.problem_link)+'" id="problem-link-element">').appendTo(roundBox);			
	    			var detailsParagraph = $('<p align="justify">').appendTo(problemLink);
	    			if(typeof obj.minimum_required_reputation !== "undefined")
	    			{
	    				if( /Android|webOS|iPad|iPhone|BlackBerry/i.test(navigator.userAgent)== false)
	    				{
	    					$('<strong>Minimum required reputation: </strong>'+String(obj.minimum_required_reputation)+'<br/>').appendTo(detailsParagraph);
	    				}
	    				else
	    				{
	    					$('<strong><i class="fa fa-copyright fa-lg" aria-hidden="true"></i>:<font color="orange">'+String(obj.minimum_required_reputation)+'</strong></font><br/>').appendTo(detailsParagraph);
	    				}
	    			}	
	    			$('<strong>Place: </strong>'+String(obj.place)+'<br/>').appendTo(detailsParagraph);
	    			$('<strong>Deadline: </strong>'+String(obj.deadline)+'<br/>').appendTo(detailsParagraph);
	    			if( /Android|webOS|iPad|iPhone|BlackBerry/i.test(navigator.userAgent)== false)
	    			{
	    				$('<strong>Description: </strong>'+String(obj.description)+'<br/>').appendTo(detailsParagraph);
	    			}
	    			
	    			if(Number(obj.bounty)>0)
	    			{
	    				$('<strong><i class="fa fa-gift fa-lg" aria-hidden="true"></i>:<font color="green">'+String(obj.bounty)+'</strong></font>').appendTo(detailsParagraph);
	    			}
	    			var tags = $('<strong>Tags: </strong>').appendTo(problemLink);
	    			$.each(obj.tags, function(i, tagObj)
	    			{
	    				//console.log("text: "+tagObj.tag_text+"tag_link: "+tagObj.tag_link);
	    				$('<a href='+String(tagObj.tag_link)+'>'+String(tagObj.tag_text)+" "+'</a>').appendTo(tags);
	    			});
	    			$('<br/>').appendTo(innerCol);
	    			
	    		});
	    		$('#'+appendElementId+'').replaceWith(appendElement);
		    }
		});
	});
}