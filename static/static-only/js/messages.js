// make an ajax call here

$(document).ready( function() {
    setTimeout(startup,1);
});

function startup() {
	/*
    $.ajax({
        url:"/async_messages/",
        type: 'GET',
        dataType: 'json',
        success: function(data){
            if( data['new_message'] ) {
            	var messages = document.getElementById('messages');
            	console.log(messages);
            	messages.html('<strong><u>Messages</u></strong>');
            }
        }
    });

	setTimeout(startup,1000*3);
	*/
}

$('messages').on('click',function(){
	var messages = document.getElementById('messages');
	console.log(messages);
	messages.html('Messages');
});