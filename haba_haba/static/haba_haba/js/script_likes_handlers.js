function ajaxLikePressedPost(_url, _post) {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: "POST",
        url: _url,
        dataType: 'json',
        data: {'post': _post},
        headers: {'X-CSRFToken': csrftoken},
        success: function callback(response) {
            let el = document.getElementById(response.object_count)
            let el_heart = document.getElementById(response.object)
            if (response.result === 1) {
                toggle_class(el_heart, 'bi-heart-fill', 'bi-heart')
                el.innerHTML = response.post_like_count
            } else if (response.result === 0) {
                toggle_class(el_heart, 'bi-heart', 'bi-heart-fill')
                el.innerHTML = response.post_like_count
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
                let el = document.getElementById(response.object_count)
                let el_heart = document.getElementById(response.object)
                if (response.result === 1) {
                    toggle_class(el_heart, 'bi-heart-fill', 'bi-heart')
                    el.innerText = response.comment_likes_count
                } else if (response.result === 0) {
                    toggle_class(el_heart, 'bi-heart', 'bi-heart-fill')
                    el.innerText = response.comment_likes_count
                }
            }
        }
    )
    ;
}