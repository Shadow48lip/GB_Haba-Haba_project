
function ajaxGetNewComplaints() {
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: '/newcomplaints/',
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken},
        success: function callback(response) {
            document.getElementById('notification_id').innerText = '('+response.object+')';
        }
    })
}



setInterval(function() {
	ajaxGetNewComplaints();
}, 100000);