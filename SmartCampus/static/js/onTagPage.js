var urlParameter= getUrlParameter("tag", document.URL);
createProblemList("tag_filter_classic_problem_list", "/get_problems_by_tag-"+urlParameter+"-classic.json");
createProblemList("tag_filter_confidence_problem_list", "/get_problems_by_tag-"+urlParameter+"-confidence.json");
