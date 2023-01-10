const wrapper = document.querySelector('.wrapper')
const iconMenu = document.querySelector('.menu-icon');

const minOffset = 50;

// изменить стили Header при скролле
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


// ??? что это должно делать и где?
// $(function () {
//     document.getElementById('a_comment_tag').scrollIntoView({
//         behavior: 'smooth',
//         block: 'start'
//     })
// })


// удалить/добавить класс
function toggle_class(el, add_class, remove_class) {
    el.classList.remove(remove_class);
    el.classList.add(add_class);
}


// прикрутить стили к лейблам Тегов
$('#custom-tags-labels label').each(function () {
    $(this).addClass('btn btn-outline-primary btn-sm m-1')
})
// менять стили при выборе Тега
const $tagStyle = $('.custom-btn-check')
$tagStyle.click(function () {
    if ($(this).prop('checked')) {
        $(this).parent().addClass('active');
    } else {
        $(this).parent().removeClass('active');
    }
});
// применить стили для активного Тега (checked)
$tagStyle.each(function () {
    if ($(this).prop('checked')) {
        $(this).parent().addClass('active');
    }
});
// вывод имени выбранного файла в input[file]
$('.input-file input[type=file]').on('change', function () {
    let file = this.files[0];
    $(this).closest('.input-file').find('.input-file-text').html(file.name);
});


// вызов search-box
const $searchInput = $('#search-input')
$('#btn-search').click(() => {
    $searchInput.toggleClass('hide-search-input')
    $searchInput.focus()

    if ($searchInput.hasClass('hide-search-input')) {
        $('.btn-search-li').css({
            'background': 'transparent',
            'border-radius': '6px',
            'transition': '.3s'
        })
    } else {
        $('.btn-search-li').css({
            'background': 'rgba(13, 110, 253, .1)',
            'border-radius': '6px',
            'transition': '.3s'
        })
    }
})
// вызов со страницы 404
$('#searchbox').click(() => {
    $('#btn-search').click()
})