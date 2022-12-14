function ajaxRegister() {
    $('#register_form_modal').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                if (response.status === 201) {
                    window.location.reload()
                } else if (response.status === 400) {
                    $('.error-auth').text(response.error).removeClass('d-none')
                }
            },
        })
    })
}

function ajaxLogin() {
    $('#login_form_modal').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                if (response.status === 201) {
                    window.location.reload()
                } else if (response.status === 400) {
                    $('.error-auth').text(response.error).removeClass('d-none')
                }
            },
        })
    })
}

function ajaxLogout() {
    const csrftoken = getCookie('csrftoken');

    $('#logout').on('click', function (e) {
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: $(this).attr('href'),
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            success: function () {
                window.location.reload()
            },
        })
    })
}

$(document).ready(function () {
    ajaxRegister()
    ajaxLogin()
    ajaxLogout()
})