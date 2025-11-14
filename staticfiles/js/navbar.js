let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');
const announcement = document.querySelector('.announcement');

window.addEventListener('scroll', function() {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;

    if (currentScroll > lastScrollTop) {

        navbar.style.transform = 'translateY(-170%)';
        announcement.style.transform = 'translateY(-100%)';
    } else {

        navbar.style.transform = 'translateY(0)';
        announcement.style.transform = 'translateY(0)';
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});

window.onload = function() {
    window.scrollTo(0, 0);
};