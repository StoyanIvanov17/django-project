const navbar = document.querySelector('.navbar');
const announcement = document.querySelector('.announcement');

window.addEventListener('scroll', function () {
    if (window.scrollY > 10) {
        announcement.classList.add('hide');
        navbar.classList.add('sticky');
    } else {
        announcement.classList.remove('hide');
        navbar.classList.remove('sticky');
    }
});

window.onload = function () {
    window.scrollTo(0, 0);
};
