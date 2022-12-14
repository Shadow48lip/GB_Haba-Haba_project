function ajaxDeleteComment(_url, _comment) {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: "POST",
        url: _url,
        dataType: 'json',
        data: {'comment_id': _comment},
        headers: {'X-CSRFToken': csrftoken},
        success: function callback(response) {
            document.getElementById('commentList_' + response.comment_id).remove();
            document.getElementById('commentListFooter_' + response.comment_id).remove();
        }
    })
}