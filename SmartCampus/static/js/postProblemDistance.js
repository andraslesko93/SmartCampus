function postProblemDistance(distance)
{
	//console.log(distance);
	$.ajax({
		type: 'POST',
	    url: "/post_problem_disctance/",
	    dataType: "json",
	    data: {
	    	'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
	    	'maxProblemDisctance': distance,
	    },
		success: function () {
			console.log("Ok");
		}
	});
	createProblemList("classic_problem_list", "/get_problems-in_time-classic.json");
	createProblemList("confidence_problem_list", "/get_problems-in_time-confidence.json");
}