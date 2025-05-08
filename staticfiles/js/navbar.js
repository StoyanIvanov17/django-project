let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;

    if (currentScroll > lastScrollTop) {

        navbar.style.transform = 'translateY(-100%)';
    } else {

        navbar.style.transform = 'translateY(0)';
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});

window.onload = function() {
    window.scrollTo(0, 0);
};