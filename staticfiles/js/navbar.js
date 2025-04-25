document.addEventListener("DOMContentLoaded", function() {
    const navbar = document.querySelector(".navbar");
    const hero = document.querySelector(".hero-video-section");

    if (!hero) {
        navbar.classList.add("scrolled");
        return;
    }

    if (!navbar) return;

    window.addEventListener("scroll", function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});
