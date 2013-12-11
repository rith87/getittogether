function update_score(postId, data)
{
    // get score
    var post = '#' + postId;
    // alert (data)
    var newScore = $(data).find(post)
    alert (newScore.text())
    
    // update score
}

function handle_vote(postId, upvote)
{
    // WTF? The key is not a string??
    var vote = upvote ? { upvote : postId } 
                : { downvote : postId };
    $.post('/', 
        vote
        ).done(
        function(data)
        {
            update_score(postId, data);
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