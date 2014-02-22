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

function add_annotation_handler()
{
    anno.addHandler('onAnnotationCreated', function(annotation) {
        annotations = anno.getAnnotations();
        var notes = '';
        for (var i = 0; i < annotations.length; i++)
        {
            notes += (JSON.stringify(annotations[i]) + ';');
        }
        jQuery('input[name=notes]').val(notes);
    });
}

// Annotorious takes the DOM object as input, so we need to do 
// $('.annotatable')[0] because $('.annotatable') will return the
// jquery object instead.
var annotation;
jQuery.noConflict();
jQuery(document).ready(function($) {
	var annotations;
	// TODO: Will this be valid in the partial post?
	var postId = $('input[name=postId]').val();
	var params = {
		postId : postId,
	};
    $('.annotatable').load(function ()
    {
        anno.makeAnnotatable($('.annotatable')[0]);        
        $.get('/notes', params)
            .done(
                function(data)
                {
                    // console.log(data);
                    // probably need to add annotations asynchronously
                    add_annotation(data);
                }
            );        
    });
    add_annotation_handler();
    $('.editable').bind('dblclick',
        function(){
            $(this).attr('contentEditable',true);
    }).blur(
        function() {
            $(this).attr('contentEditable', false);
            $('input[name=' + $(this).attr('name') + ']').val($(this).text());
    });    
});

