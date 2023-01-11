function ajaxBadPost(_url, _post) {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: "POST",
        url: _url,
        dataType: 'json',
        data: {'post_id': _post},
        headers: {'X-CSRFToken': csrftoken},
        success: function callback(response) {
            let el = document.getElementById('bad_post_' + response.object)
            if (response.complaint === 1) {
                toggle_class(el, 'bi-exclamation-circle-fill', 'bi-exclamation-circle')
            } else if (response.complaint === 0) {
                toggle_class(el, 'bi-exclamation-circle', 'bi-exclamation-circle-fill')
            }
        }
    })
}