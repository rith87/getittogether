function parse_notes(notes)
{
    var parsedNotes = notes.split(";");
    parsedNotes.splice(parsedNotes.length - 1, 1);
    return parsedNotes;
}

function add_annotation(data)
{
	// TODO: Does this conflict with Jquery?
	if (data)
	{
        // alert(data);
        var parsedNotes = parse_notes(data);
        for (var i = 0; i < parsedNotes.length; i++)
        {
            // alert(parsedNotes[i]);
            anno.addAnnotation(JSON.parse(parsedNotes[i]));
        }
	}
}

var annotation;
jQuery.noConflict();
jQuery(document).ready(function($) {
	var annotations;
	// TODO: Will this be valid in the partial post?
	var postId = $('input[name=postId]').val();
	var params = {
		postId : postId,
		notes : '',
		set : 'False'
	};
    $('.annotatable').load(function ()
    {
        anno.makeAnnotatable($('.annotatable')[0]);        
        $.post('/notes', params)
            .done(
                function(data)
                {
                    console.log(data);
                    // probably need to add annotations asynchronously
                    add_annotation(data);
                }
            );        
    });
    anno.addHandler('onAnnotationCreated', function(annotation) {
        annotations = anno.getAnnotations();
        var notes = '';
        for (var i = 0; i < annotations.length; i++)
        {
            // alert(JSON.stringify(annotations[i]));
            notes += (JSON.stringify(annotations[i]) + ';');
        }
        $('input[name=notes]').val(notes);
    });
});

// TODO: Move annotorious code here if it conflicts with JQuery
// window.onload = function() {      
// }