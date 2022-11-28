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

