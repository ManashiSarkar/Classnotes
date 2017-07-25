
$(".submit").live("click", function () {
			var content = tinymce.get('id_content').getContent();
			alert(content);
            tinyMCE.triggerSave();
            //var f = $(this).parents("form");
            //var action = f.attr("action");
            //var serializedForm = f.serialize();
            //tinyMCE.triggerSave(); also tried putting here
            
    return false;
    });

/*
$(document).ready(function(){

	$('#tinymce-form').submit(function(e){

		var content = tinymce.get('texteditor').getContent();

		$('#display-form').html(content);

		return false; //to prevent page reloading, as then tinymce clears out the data
	});
});*/