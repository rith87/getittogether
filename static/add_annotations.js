function add_annotation(data)
{
	// TODO: Does this conflict with Jquery?
	if (data)
	{
		anno.addAnnotation(JSON.parse(data));
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
                    // probably need to add annotations asynchronously
                    add_annotation(data);
                }
            );        
    });
    anno.addHandler('onAnnotationCreated', function(annotation) {
        annotations = anno.getAnnotations();
        for (var i = 0; i < annotations.length; i++)
        {
            // alert(JSON.stringify(annotations[i]));
            $('input[name=notes]').val(JSON.stringify(annotations[i]));
        }
    });
});

// TODO: Move annotorious code here if it conflicts with JQuery
// window.onload = function() {      
// }