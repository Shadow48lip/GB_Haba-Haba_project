function ajaxSendComment() {
    $("#add_comment_form").submit(function (e) {
        e.preventDefault()
        let get_comment_text = document.querySelector('#postReply');
        let get_post_id = document.querySelector('#add_comment_form').getAttribute('data-post-id');
        const csrftoken = getCookie('csrftoken');

        $.ajax({
            type: this.method,
            url: this.action,
            dataType: 'json',
            data: {
                'text': get_comment_text.value,
                'post': get_post_id,
            },
            headers: {'X-CSRFToken': csrftoken},
            success: function callback(response) {
                $("#comment").append(response.data)
                get_comment_text.value = '';
                document.querySelector('#comment_count_id').innerHTML = 'Комментарии (' + response.comment_count + ')';
            }
        })
    })
}

$(document).ready(function () {
    ajaxSendComment()
})
