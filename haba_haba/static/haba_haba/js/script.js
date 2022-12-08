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


// сохраненить/полученить данные о пользовательской теме (light/dark)
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
function auto_grow(element) {
    element.style.height = "6em";
    element.style.height = (element.scrollHeight) + "px";
};


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
$(document).ready(function () {
    $(function ($) {
        $('#login_form_modal').submit(function (e) {
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
    })
})

$(document).ready(function () {
    $(function ($) {
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
    })
});