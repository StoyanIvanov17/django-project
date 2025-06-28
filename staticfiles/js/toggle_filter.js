document.addEventListener("DOMContentLoaded", function () {
    const productsGalleryWrapper = document.querySelector(".products-gallery-wrapper");
    const toggleBtn = document.getElementById("toggle-filter");

    if (!toggleBtn) return;

    toggleBtn.addEventListener("click", function (e) {
        e.preventDefault();
        productsGalleryWrapper.classList.toggle("show-filters");
        toggleBtn.innerHTML = productsGalleryWrapper.classList.contains("show-filters")
            ? 'Hide Filters <i class="fa-solid fa-filter"></i>'
            : 'Show Filters <i class="fa-solid fa-filter"></i>';
    });
});
