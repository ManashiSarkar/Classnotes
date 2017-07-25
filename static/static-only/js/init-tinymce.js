tinymce.init({
	selector: 'textarea.tinymce',
	setup: function (editor) {
        editor.onChange.add(function() {
            editor.save();
        });
    }
})
