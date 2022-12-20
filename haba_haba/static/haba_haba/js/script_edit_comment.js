function ajaxEditComment() {
    let buttons = document.querySelectorAll('span[data-id]');

    buttons.forEach((btn) => {
        btn.addEventListener('click', edit);
    })
}

function get_id_num(id) {
    return id.substring(17, 50)
}

function edit() {
    let id = get_id_num(this.id)
    let comment_text = document.getElementById('text_area_' + id);
    comment_text.contentEditable = true;

    toggle_class(document.getElementById('icon_edit_' + id), 'bi-pencil-fill', 'bi-pencil');
    this.addEventListener('click', send);
}

function send() {
    const csrftoken = getCookie('csrftoken');
    let id = get_id_num(this.id)
    let comment_text = document.getElementById('text_area_' + id);
    comment_text.contentEditable = false;

    $.ajax({
        type: "POST",
        url: $(this).data('url'),
        dataType: 'json',
        data: {
            'comment_id': id,
            'comment_text': comment_text.textContent
        },
        headers: {'X-CSRFToken': csrftoken},
        success: function callback(response) {
            toggle_class(document.getElementById('icon_edit_' + id), 'bi-pencil', 'bi-pencil-fill');
            comment_text.contentEditable = false;
        }
    })
    this.removeEventListener('click', send);
    toggle_class(document.getElementById('icon_edit_' + id), 'bi-pencil', 'bi-pencil-fill');
}

ajaxEditComment()