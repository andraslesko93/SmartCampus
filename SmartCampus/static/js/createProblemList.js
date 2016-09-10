function createProblemList (appendElementId, jsonLink)
{
	
	$.getJSON(jsonLink, function(data)
	{
		if(data.length==0)
			{
			return;
			}
		var col = $('<div class ="col-xs-12 col-md-6">').appendTo("#"+appendElementId);
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
			
			var userLink = $('<a href='+String(obj.user_link)+' id="user-link-element"> <img src="'+String(obj.picture)+'" width="50"/> </a>').appendTo(roundBox);
			$('<strong>'+String(obj.user)+': </strong>').appendTo(userLink);	
			var problemLink = $('<a href="'+String(obj.problem_link)+'" id="problem-link-element">').appendTo(roundBox);
			$('<strong>'+String(obj.title)+'</strong> <br/>').appendTo(problemLink);

			
		
			
			if(typeof obj.minimum_required_reputation !== "undefined")
			{
				if( /Android|webOS|iPad|iPhone|BlackBerry/i.test(navigator.userAgent)== false)
				{
					$('<strong>Minimum required reputation: </strong>'+String(obj.minimum_required_reputation)+'<br/>').appendTo(problemLink);
				}
				else
				{
					$('<strong><i class="fa fa-copyright fa-lg" aria-hidden="true"></i>:<font color="orange">'+String(obj.minimum_required_reputation)+'</strong></font><br/>').appendTo(problemLink);
				}
			}
			
		
			var paragraph = $('<p align="justify">').appendTo(problemLink);
			$('<strong>Deadline: </strong>'+String(obj.deadline)+'<br/>').appendTo(paragraph);
			if( /Android|webOS|iPad|iPhone|BlackBerry/i.test(navigator.userAgent)== false)
			{
				$('<strong>Description: </strong>'+String(obj.description)+'<br/>').appendTo(paragraph);
			}
			$('<br/>').appendTo(innerCol);
			
			if(Number(obj.bounty)>0)
			{
				$('<strong><i class="fa fa-gift fa-lg" aria-hidden="true"></i>:<font color="green">'+String(obj.bounty)+'</strong></font><br/>').appendTo(problemLink);
			}
			
			var tags = $('<strong>Tags: </strong>').appendTo(problemLink);
			$.each(obj.tags, function(i, tagObj)
			{
				//console.log("text: "+tagObj.tag_text+"tag_link: "+tagObj.tag_link);
				$('<a href='+String(tagObj.tag_link)+'>'+String(tagObj.tag_text)+" "+'</a>').appendTo(tags);
			}		
			);
			
		});
	});
}
