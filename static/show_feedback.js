function update_score(postId)
{
    var post = '#' + postId;
    alert($(post).text())
}

function handle_vote(postId, upvote)
{
    // WTF? The key is not a string??
    var vote = upvote ? { upvote : postId } 
                : { downvote : postId };
    $.post('/', 
        vote
        ).done(
        function()
        {
            update_score(postId);
        }
    );
}

$(document).ready(function(){
    $("#msgid").html("Hello World from JQuery");
    $(".vote").click(function()
        {
            handle_vote($(this).attr('value'), 
                $(this).attr('name') == 'upvote')
        }
    );
});