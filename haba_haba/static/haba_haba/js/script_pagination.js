function ajaxPagination() {
    $('#pagination a.page-link').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()
            let page_url = $(el).attr('href')
            $.ajax({
                url: page_url,
                type: 'GET',
                success: (data) => {
                    // устанавливаем URL в строку браузера
                    window.history.pushState({route: page_url}, "", page_url);
                    // на место старых данных ставим новые данные и обновляем блок пагинации
                    $('#cards').empty().append($(data).find('#cards').html())
                    $('#pagination').empty().append($(data).find('#pagination').html())
                    // скроллим страницу в начало
                    $(window).scrollTop(0)
                }
            })
        })
    })
}

$(document).ready(function () {
    ajaxPagination()
})
$(document).ajaxStop(function () {
    ajaxPagination()
})