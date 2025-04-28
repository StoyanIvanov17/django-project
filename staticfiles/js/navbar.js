document.addEventListener("DOMContentLoaded", function() {
    const navbar = document.querySelector(".navbar");
    const hero = document.querySelector(".hero-video-section");

    if (!navbar) return;

    if (hero) {
        const heroHeight = hero.offsetHeight;

        window.addEventListener("scroll", function() {
            if (window.scrollY > heroHeight - 100) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        });
    }
});
