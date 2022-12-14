function ajaxLikePressedPost(_url, _post) {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: "POST",
        url: _url,
        dataType: 'json',
        data: {'post': _post},
        headers: {'X-CSRFToken': csrftoken},
        success: function callback(response) {
            if (response.result === 1) {
                document.getElementById(response.object).classList.remove('bi-heart')
                document.getElementById(response.object).classList.add('bi-heart-fill')
                document.getElementById(response.object_count).innerHTML = response.post_like_count
            } else if (response.result === 0) {
                document.getElementById(response.object).classList.add('bi-heart')
                document.getElementById(response.object).classList.remove('bi-heart-fill')
                document.getElementById(response.object_count).innerHTML = response.post_like_count
            }
        }
    })
}


function ajaxLikePressedComment(_url, _comment) {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
            type: "POST",
            url: _url,
            dataType: 'json',
            data: {'comment': _comment},
            headers: {'X-CSRFToken': csrftoken},
            success: function callback(response) {
                if (response.result === 1) {
                    document.getElementById(response.object).classList.remove('bi-heart')
                    document.getElementById(response.object).classList.add('bi-heart-fill')
                    document.getElementById(response.object_count).innerHTML = response.comment_likes_count
                } else if (response.result === 0) {
                    document.getElementById(response.object).classList.add('bi-heart')
                    document.getElementById(response.object).classList.remove('bi-heart-fill')
                    document.getElementById(response.object_count).innerHTML = response.comment_likes_count
                }
            }
        }
    )
    ;
}