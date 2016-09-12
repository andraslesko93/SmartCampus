$.getJSON("/get_ratings-rate_solution_author.json", function(data)
		{
			if(data.length==0)
				{
					return;
				}
			$.each(data, function(i, obj) 
			{
				var row = $('<div class ="row">').appendTo('#rate_solution_authors');
				var col = $('<div class ="col-md-6 col-xs-12">').appendTo(row);
			});
		});
	
$.getJSON("/get_ratings-rate_problem_author.json", function(data)
		{
			if(data.length==0)
			{
				return;
			}
			
			$.each(data, function(i, obj) 
			{
				var row = $('<div class ="row">').appendTo('#rate_problem_authors');
				var col = $('<div class ="col-md-6 col-xs-12">').appendTo(row);
			});
		});



/*{% for rate_solution_author  in rate_solution_authors %}
			
			<div class="row">
			<div class="col-xs-12">
			<div class="round-box"> 
			
		        	<h4>
						<a href="/users/{{ rate_solution_author.rated_user.userprofile.slug }}">
		        			<img src="{{rate_solution_author.rated_user.userprofile.picture_url}}" width="50"/>
		        		</a>
		        			<strong><a href="/users/{{ rate_solution_author.rated_user.userprofile.slug }}">{{rate_solution_author.rated_user}}</a></strong>  
		        			offered a solution to your problem:
		        			<strong><a href="/problems/{{ rate_solution_author.solution.problem_id.slug }}"> {{ rate_solution_author.solution.problem_id.title }} </a></strong>
		        			, and you accepted it.
					</h4>
					
					<strong>Served people:</strong> {{rate_solution_author.solution.served_ppl}} <br/>
					<strong>Description:</strong> {{rate_solution_author.solution.desc}} <br/>
		        	<br/>
					
		        	<form id = "rate_sol_auth_from_singl" action="" method="POST">
		        		{% csrf_token %}
		        		{{rate_problem_author.pk}}
		        		<input type = "hidden" name = "rate_solution_author" value = "{{rate_solution_author.pk}}"/>
		        		
		        		{%if rate_solution_author.solution.served_ppl == 1 %}
		        		<strong>Has {{rate_solution_author.rated_user}} appeared?</strong>
	  					<br/>
	  					<input type="radio" name="appeared" value="no">no &nbsp;
	  					<input type="radio" name="appeared" value="yes" checked>yes
						<br/>
						<br/>
						<strong>Please rate {{rate_solution_author.rated_user}}'s behaviour during the process!</strong>
	  					<br/>
	  					<input type="radio" name="behaviour" value="1">Bad &nbsp;
	  					<input type="radio" name="behaviour" value="2" checked>Average &nbsp;
	  					<input type="radio" name="behaviour" value="3">Good
						<br/>
						<br/>
						<strong>How helpful was it?</strong>
	  					<br/>
	  					<input type="radio" name="helpful" value="1">Not so helpful &nbsp;
	  					<input type="radio" name="helpful" value="2" checked>Average &nbsp;
	  					<input type="radio" name="helpful" value="3">Very helpful 
						<br/>
						<br/>
						<strong>Will you accept any further help from {{rate_solution_author.rated_user}} in the future?</strong>
	  					<br/>
	  					<input type="radio" name="further_help" value="1">No &nbsp;
	  					<input type="radio" name="further_help" value="2" checked>Maybe &nbsp;
	  					<input type="radio" name="further_help" value="3">Yes
	  					<br/>
	  					<br/>
	  					<button type="submit" class="btn btn-xs btn-primary">Rate {{rate_solution_author.rated_user}}</button>						
						
						{%else%}
						<strong>How many people did {{rate_solution_author.rated_user}} serve? (between 0 and {{rate_solution_author.solution.served_ppl}})</strong>
						<br/>
  						<input type="number" name="appeared_people" min="0" max="{{rate_solution_author.solution.served_ppl}}">
  						
  						<br/>
						<br/>
						<strong>Please rate {{rate_solution_author.rated_user}} and its crew's behaviour during the process!</strong>
	  					<br/>
	  					<input type="radio" name="behaviour" value="1">Bad &nbsp;
	  					<input type="radio" name="behaviour" value="2" checked>Average &nbsp;
	  					<input type="radio" name="behaviour" value="3">Good
						<br/>
						<br/>
						<strong>How helpful were they?</strong>
	  					<br/>
	  					<input type="radio" name="helpful" value="1">Not so helpful &nbsp;
	  					<input type="radio" name="helpful" value="2" checked>Average &nbsp;
	  					<input type="radio" name="helpful" value="3">Very helpful 
						<br/>
						<br/>
						<strong>Will you accept any further help from {{rate_solution_author.rated_user}} in the future?</strong>
	  					<br/>
	  					<input type="radio" name="further_help" value="1">No &nbsp;
	  					<input type="radio" name="further_help" value="2" checked>Maybe &nbsp;
	  					<input type="radio" name="further_help" value="3">Yes
	  					<br/>
	  					<br/>
	  					<button type="submit" class="btn btn-xs btn-primary">Rate {{rate_solution_author.rated_user}}</button>
						{%endif%}
						

					</form>
					</div>
					</div>
					</div>
						<br/>*/