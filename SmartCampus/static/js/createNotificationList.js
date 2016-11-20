function createNotificationList (appendElementId, uncheckedNotificationNumber, location)
{
	var appendElement= $('<div id="'+appendElementId+'"></div>');
	var row = $('<div class="row">').appendTo(appendElement);
	jsonLink= "/get_notifications_"+String(uncheckedNotificationNumber)+".json"
	
	$.getJSON(jsonLink, function(data)
	{
		$.each(data, function(i, obj) 
		{	
			/*console.log("status: "+obj.status+
	                " picture: "+obj.picture+
	                " sender: "+obj.sender+
	                " problem_title: "+obj.problem_title+
	                " problem_link: "+obj.problem_link+
	                " model_type: "+obj.model_type+
	                " bounty: "+obj.bounty+
	                " granted_reputation: "+obj.granted_reputation+
	                " reputation: "+obj.reputation);*/
			status = String(obj.status);
			var col = document.createElement('div');
			col.className="col-xs-12";
			row.append(col);		
				var problemLink = document.createElement('a');
				problemLink.setAttribute('href', String(obj.problem_link));
				problemLink.setAttribute('id', "notification-link-element");
				col.appendChild(problemLink);
					var notificationItem= document.createElement('div');
					if(String(obj.status)=="checked")
					{
						notificationItem.className="checked-notification-item";
					}
					else
					{
						notificationItem.className="unchecked-notification-item";
					}
					problemLink.appendChild(notificationItem);
					
					var innerRow = $('<div class="row">');
					innerRow.appendTo(notificationItem);
					var imageCol;
					var textCol;
					if(location == "dropdown_menu")
					{
						imageCol = $('<div class="col-xs-2" align="center">');
						textCol = $('<div class="col-xs-10">');
					}
					else if(location == "full_page")
					{
						imageCol = $('<div class="col-xs-1" align="center">');
						textCol = $('<div class="col-xs-11">');
					}	
					imageCol.appendTo(innerRow);
					$('<img src='+String(obj.picture)+' width="50" style="vertical-align:middle";>').appendTo(imageCol);
					textCol.appendTo(innerRow);	
					var textnode=$('<p>');
					textnode.appendTo(textCol);
					textnode.append('<strong>'+String(obj.sender)+'</strong>');
					
						if (String(obj.model_type)=="accepted solution")
							{
								textnode.append(" accepted your solution, to the problem: ");
							}
						else if (String(obj.model_type)=="offered solution")
							{
								textnode.append(" offered you a solution to your problem: ");
							}
						else if (String(obj.model_type)=="rate solution author")
							{
								textnode.append(" rated your help in his problem: ");
							}
						else if (String(obj.model_type)=="rate problem author")
							{
								textnode.append(" rated you, after the helping in your problem: ");
							}
						else if (String(obj.model_type)=="user")
							{
								textnode.append(" Welcome to SmartCampus, an ideal place to solve your problems and help others! Please allow me to help you to discover the application. :)");
							}
						if (typeof obj.problem_title!=="undefined")
						{
							textnode.append('<i>'+String(obj.problem_title)+"."+'</i>');
						}
						if (Number(obj.granted_reputation)<Number(obj.reputation))
						{
							textnode.append('<br/>');
							textnode.append('<small>'+" You gained"+String(obj.granted_reputation)+" reputation point from "+String(obj.reputation)+". You are so awesome, that you managed to reach the daily reputation limit! :)"+'</small>');
						}
						else if (Number(obj.granted_reputation)>=Number(obj.reputation))
						{
							textnode.append('<br/>');
							textnode.append('<small>'+" You gained "+String(obj.granted_reputation)+" reputation point."+'</small>');
						}
						if (Number(obj.bounty)>0)
						{
							textnode.append('<br/>');
							textnode.append('<small>'+" You also gained "+String(obj.bounty)+" reputation point from the bounty of the problem."+'</small>');
						}
		});
	});
	$('#'+appendElementId+'').replaceWith(appendElement);
}
