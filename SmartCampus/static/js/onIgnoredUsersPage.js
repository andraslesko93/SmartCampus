var col= $('<div class ="col-xs-12 col-md-5">').appendTo("#ignored_users_list");
var roundBox=$('<div class="round-box">').appendTo(col);

$.getJSON("/get_ignored_users.json", function(data)
{
	if (data.length==0)	
	{
		$('<h7>You dont have any issues with others :)</h7>').appendTo(roundBox);
	}
	$.each(data, function(i, obj) 
	{
		var hFour=$('<h4>').appendTo(roundBox);
		var name=$('<c>'+String(obj.username)+' </c>').appendTo(hFour);		
		var button=$('<button type="submit" class="btn btn-success">Unblock</button>').appendTo(hFour);
		button.click(function() { 
	        $.ajax({
	            url: document.url,
	            type: 'POST',
	            dataType: "json",
	            data: {'id':obj.id, 'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
	            success: function (result) {
	              console.log("OK");
	              }
	        });
	        hFour.hide();

	});
	}
	);
});