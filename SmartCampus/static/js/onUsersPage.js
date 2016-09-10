var urlParameter= getUrlParameter("users", document.URL);

$.getJSON("/get_user_details_by_id-"+urlParameter+".json", function(data)
	{
    if (data.length == 0 )
    {
        $("#ignore_button").hide();
        return;
    }
	console.log("picture: "+data.picture+
			"username: "+data.username+ 
			"email: " + data.email+ 
			"joined_at: "+ data.joined_at+ 
			"last_login: "+data.last_login+ 
			"reputation: "+data.reputation);
	$('<img src='+String(data.picture)+' width="200"/> <br>').appendTo("#user_details");
	$('<br/> <c><strong>Username: </strong>'+String(data.username)+'</c>').appendTo("#user_details");
	$('<br/> <c><strong>Email address: </strong>'+String(data.email)+'</c>').appendTo("#user_details");
	$('<br/> <c><strong>Joined at: </strong>'+String(data.joined_at)+'</c>').appendTo("#user_details");
	$('<br/> <c><strong>Last login: </strong>'+String(data.last_login)+'</c>').appendTo("#user_details");
	$('<br/> <c><strong>Reputation: </strong>'+String(data.reputation)+'</c>').appendTo("#user_details");
	
	if(String(data.ignore)=="allowed") 
	{
		$('<br/><br/>').appendTo('#user_details');
		var button=$('<button type ="submit" class="btn btn-primary btn-danger">Ignore <i class="fa fa-minus" aria-hidden="true"></i></button>	').appendTo("#user_details");
		button.click(function() { 
	        $.ajax({
	            url: document.url,
	            type: 'POST',
	            dataType: "json",
	            data: {'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
	            success: function (result) {
	              console.log("OK");
	              }
	        });
	        button.hide();
	        $('<c><font color="red">You successfully ignored this user! </font></c>').appendTo("#user_details");
		});
	}
	});