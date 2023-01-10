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
            let tag_id = document.getElementById('comment_count_id');
            tag_id.innerHTML = 'Комментарии ('+response.comment_count+')';
        }
    })
}
