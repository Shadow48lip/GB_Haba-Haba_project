const body = document.querySelector('body')
const wrapper = document.querySelector('.wrapper')
const toggleTheme = document.querySelector('.theme-switch');
const iconMenu = document.querySelector('.menu-icon');
const minOffset = 100;


// показать/спрятать Header при скролле
window.onscroll = function () {
    let is_scrolled = wrapper.classList.contains("is_scrolled");

    if (minOffset < document.documentElement.scrollTop) {
        if (!is_scrolled) {
            wrapper.classList.add("is_scrolled");
        }
    } else if (is_scrolled) {
        wrapper.classList.remove("is_scrolled")
    }
}


// сохранить/получить данные о пользовательской теме (light/dark)
toggleTheme.addEventListener('click', () => {
    body.classList.toggle('dark');
    localStorage.setItem('theme', body.classList);
});

window.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark');
    } else {
        body.classList.remove('dark');
    }
});


// автоматическое изменение высоты Textarea
$(document).on("input", "textarea", function () {
    $(this).outerHeight(38).outerHeight(this.scrollHeight);
});


// кнопка меню Burger (мобильные устройства)
if (iconMenu) {
    iconMenu.addEventListener('click', () => {
        iconMenu.classList.toggle('_active');
    });
}


// календарь
$(function () {
    $('input[name="datetimes"]').daterangepicker({
        timePicker: true,
        timePickerIncrement: 5,
        timePicker24Hour: true,
        showDropdowns: true,
        startDate: moment().startOf('hour'),
        endDate: moment().startOf('hour').add(24, 'hour'),
        locale: {
            format: 'DD/MM/YYYY HH:mm',
            daysOfWeek: ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'],
            monthNames: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            firstDay: 0,
            applyLabel: 'Принять',
            cancelLabel: 'Отмена',
        }
    });
});


// мозги для модального окна (почему-то не работает одна функция на две модалки...)
function ajaxRegister() {
    $('#register_form_modal').submit(function (e) {
        e.preventDefault()
        // console.log('this: ', this)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                // console.log('ok: ', response)
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
        // console.log('this: ', this)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                if (response.status === 201) {
                    // console.log('ok: ', response)
                    window.location.reload()
                } else if (response.status === 400) {
                    // console.log('err: ', response)
                    $('.error-auth').text(response.error).removeClass('d-none')
                }
            },
        })
    })
}

function ajaxLogout() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $('#logout').on('click', function (e) {
        e.preventDefault()
        // console.log('this: ', this)
        $.ajax({
            type: 'POST',
            url: $(this).attr('href'),
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
                // console.log('ok: ', data)
                window.location.reload()
            },
        })
    })
}


// пагинация через ajax
function ajaxPagination() {
    $('#pagination a.page-link').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()
            let page_url = $(el).attr('href')
            // console.log(page_url)
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
    ajaxRegister()
    ajaxLogin()
    ajaxLogout()
    ajaxPagination()
})
$(document).ajaxStop(function () {
    ajaxRegister()
    ajaxLogin()
    ajaxLogout()
    ajaxPagination()
})