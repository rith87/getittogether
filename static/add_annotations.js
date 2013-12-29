var annotation;
jQuery.noConflict();
jQuery(document).ready(function($) {
    annotation = JSON.parse($('#test').text());
    // JQuery and annotorious conflict?
});
window.onload = function() {
    /*
    anno.addHandler('onAnnotationCreated', function(annotation) {
        annotations = anno.getAnnotations();
        for (var i = 0; i < annotations.length; i++)
        {
            // alert(JSON.stringify(annotations[i]));
            $('#test').text(JSON.stringify(annotations[i]));
        }
    });
    */
    
    // alert($('#test').text());
    // alert(annotation.text);
    anno.addAnnotation(annotation);        
}