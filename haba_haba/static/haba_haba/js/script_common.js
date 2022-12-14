const wrapper = document.querySelector('.wrapper')
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
$(function () {
    document.getElementById('comment_count_id').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    })
})


// удалить/добавить класс
function toggle_class(el, add_class, remove_class) {
    el.classList.remove(remove_class);
    el.classList.add(add_class);
}
