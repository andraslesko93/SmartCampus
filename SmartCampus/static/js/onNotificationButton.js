$('#notification_button').click(function(){
	createNotificationList("tiny_notification_list", 10, "dropdown_menu");
    $.get("/check_the_unchecked_notifications.json/", function(data){
        $('#notification_count').hide();
    });
});

/*$('#notification_button_mobile').click(function(){
	createNotificationList("tiny_notification_list", 10);
    $.get("/check_the_unchecked_notifications.json/", function(data){
        $('#notification_count').hide();
    });
});
*/