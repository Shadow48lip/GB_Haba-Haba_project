function ajaxGetNewComplaints() {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: "POST",
        url: '/newcomplaints/',
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken},
        success: function callback(response) {
            document.querySelector('#notification_id').innerText = response.object;
        }
    })
}


setInterval(
    function () {
        ajaxGetNewComplaints();
    },
    600000 // 1min
);