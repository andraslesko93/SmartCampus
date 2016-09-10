function gup( name, url ) {
  if (!url) url = location.href;
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( url );
  return results == null ? null : results[1];
}
var urlParameter= gup("query", document.URL);
createProblemList("search_problem_list","/get_problems_by_keyword/?query="+urlParameter);
$.getJSON("/get_users_by_keyword/?query="+urlParameter, function(data)
	{
	var col= $('<div class ="col-xs-12 col-md-6">').appendTo("#search_user_list");
	if(data.length==0)
	{
		$.getJSON("/get_problems_by_keyword/?query="+urlParameter, function(probdata){
			if(probdata.length==0)
			{
				var row = $('<div class ="row">').appendTo(col);
				var innerCol = $('<div class="col-xs-12">').appendTo(row);
				var roundBox = $('<div class="round-box">').appendTo(innerCol);
				$('<h4>No result for your query: '+urlParameter+'</h4>').appendTo(roundBox);
			}
		})
		return;
	}
	$.each(data, function(i, obj) {
		
		var row = $('<div class ="row">').appendTo(col);
		var innerCol = $('<div class="col-xs-12">').appendTo(row);
		var roundBox = $('<div class="round-box">').appendTo(innerCol);
		var hFour = $('<h4>').appendTo(roundBox);
		$('<a href='+String(obj.user_link)+'> <img src="'+String(obj.picture)+'" width="50"/> </a>').appendTo(hFour);
		$('<strong><a href="'+String(obj.user_link)+'">'+String(obj.user_name)+'</a></strong>').appendTo(hFour);
		$('<strong>Reputation:</strong> <c>'+String(obj.reputation)+'</c>').appendTo(roundBox);
		$('<br/>').appendTo(innerCol);
	});

});