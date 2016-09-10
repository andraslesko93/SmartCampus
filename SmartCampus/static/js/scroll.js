if( /Android|webOS|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
	$('#add-button-desktop').hide();
	var addButtonMobile=$('<button onclick="location.href = \'/add_problem/\';" type="button" class="btn btn-primary-outline btn-circle btn-xl"><i class="fa fa-plus fa-lg"></i></button>').appendTo('#add-button-mobile');
	var previousScroll = 0,
		headerOrgOffset = $('#header').height();
	$('#header-wrap').height($('#header').height());

	$(window).scroll(function () {
		var currentScroll = $(this).scrollTop();
		if (currentScroll > headerOrgOffset) {
			if (currentScroll > previousScroll) {
				$('#header-wrap').slideUp();
				$('#add-button-mobile').slideUp();
			} else {
				$('#header-wrap').slideDown();
				$('#add-button-mobile').slideDown();
			}
		} 
		previousScroll = currentScroll;
	});

}