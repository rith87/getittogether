function update_score(postId, data)
{
    // get score from post request
    var post = '#' + postId;
    var newScore = $(data).find(post);
    
    // update score
    $(post).text (newScore.text());
}

function handle_vote(postId, upvote)
{
    // vote is a javascript object with data member up/downvote
    // and its value is set to postId
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
    $(".vote").click(function()
        {
            handle_vote($(this).attr('value'), 
                $(this).attr('name') == 'upvote')
        }
    );
});