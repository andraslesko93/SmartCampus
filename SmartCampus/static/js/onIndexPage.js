createProblemList("classic_problem_list", "/get_problems-in_time-classic.json");
createProblemList("confidence_problem_list", "/get_problems-in_time-confidence.json");


$.getJSON("/tag_cloud.json", function(data)
{
	$.each(data, function(i, obj) 
	{
		$('<strong> <a href='+String(obj.link)+' class="tagCloud-'+String(obj.weight)+'">'+String(obj.text)+'</a> </strong>').appendTo("#tagCloud");
	}
	);
});