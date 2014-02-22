// paste screenshot:
// http://stackoverflow.com/questions/6333814/how-does-the-paste-image-from-clipboard-functionality-work-in-gmail-and-google-c
// http://strd6.com/2011/09/html5-javascript-pasting-image-data-in-chrome/

// prepare the form when the DOM is ready 
jQuery.noConflict();
jQuery(document).ready(function($) { 
    var options = { 
        // target:        '#output1',   // target element(s) to be updated with server response 
        beforeSubmit:   showRequest,     // pre-submit callback 
        success:        showResponse    // post-submit callback 
 
        // other available options: 
        //uploadProgress: handle_upload_progress    // re-enable for progress bar
        //url:       url         // override for form's 'action' attribute 
        //type:      type        // 'get' or 'post', override for form's 'method' attribute 
        //dataType:  null        // 'xml', 'script', or 'json' (expected server response type) 
        //clearForm: true        // clear all form fields after successful submit 
        //resetForm: true        // reset the form after successful submit 
 
        // $.ajax options can be used here too, for example: 
        //timeout:   3000 
    }; 
 
    // bind form using 'ajaxForm' 
    $('.add-feedback').ajaxForm(options);

    document.onpaste = function(event){
        var items = (event.clipboardData || event.originalEvent.clipboardData).items;
        console.log(JSON.stringify(items)); // will give you the mime types
        var blob = items[0].getAsFile();
        var reader = new FileReader();
        reader.onload = function(event){
            console.log(event.target.result);
            var ss = $('<img />').attr({'src' : event.target.result, 'class' : 'annotatable'});
            $('#screenshot').append(ss);
            // NOTE: image is autoscaled?
            ss.height(ss.height() / 2);           
            // ss.width(ss.width() / 2);
            $('.add-feedback').append($('<input />').attr({
                'name' : 'screenshotDataUrl', 
                'value' : event.target.result,
                'type' : 'hidden'
            }));
            anno.makeAnnotatable($('.annotatable')[0]);
            add_annotation_handler();
        }; // data url!
        reader.readAsDataURL(blob);
    }    
}); 

function handle_upload_progress(event, position, total, percentComplete)
{
    alert('Percent:' + percentComplete);
    $('#output1').text(percentComplete + '% complete');
}
 
// pre-submit callback 
function showRequest(formData, jqForm, options) { 
    // formData is an array; here we use $.param to convert it to a string to display it 
    // but the form plugin does this for you automatically when it submits the data 
    var queryString = jQuery.param(formData); 
 
    // jqForm is a jQuery object encapsulating the form element.  To access the 
    // DOM element for the form do this: 
    // var formElement = jqForm[0]; 
 
    // alert('About to submit: \n\n' + queryString); 
 
    // here we could return false to prevent the form from being submitted; 
    // returning anything other than false will allow the form submit to continue 
    return true; 
}

function update_page (responseText)
{
    var newPage = jQuery(responseText).filter('.page').children();
    jQuery('.page').html(newPage);
}
 
// post-submit callback 
function showResponse(responseText, statusText, xhr, $form)  { 
    // for normal html responses, the first argument to the success callback 
    // is the XMLHttpRequest object's responseText property 
 
    // if the ajaxForm method was passed an Options Object with the dataType 
    // property set to 'xml' then the first argument to the success callback 
    // is the XMLHttpRequest object's responseXML property 
 
    // if the ajaxForm method was passed an Options Object with the dataType 
    // property set to 'json' then the first argument to the success callback 
    // is the json data object returned by the server 
 
    // alert('status: ' + statusText + '\n\nresponseText: \n' + responseText + 
        // '\n\nThe output div should have already been updated with the responseText.'); 
    
    // Not really sure if JS is the way to go...
    // alert(responseText);
    update_page(responseText);
} 