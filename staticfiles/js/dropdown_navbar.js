function disableScroll() {
    document.body.style.overflow = 'hidden';
}

function enableScroll() {
    document.body.style.overflow = 'auto';
}

document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav-links a");
    const megaContainer = document.getElementById("megaDropdownContainer");
    const navHoverArea = document.querySelector(".navbar");

    const dropdowns = {
        "WOMEN": document.getElementById("womenDropdown"),
        "MEN": document.getElementById("menDropdown"),
        "KIDS": document.getElementById("kidsDropdown")
    };

    navLinks.forEach(link => {
        const dropdownType = link.getAttribute("data-dropdown");
        link.addEventListener("mouseenter", function () {
            const dropdown = dropdowns[dropdownType];
            if (dropdown) {
                megaContainer.classList.add("show");
                dropdown.classList.add("show");
                disableScroll();
            }
        });
    });

    megaContainer.addEventListener("mouseenter", function () {
        megaContainer.classList.add("show");
        disableScroll();
    });

    navHoverArea.addEventListener("mouseleave", function () {
        megaContainer.classList.remove("show");
        Object.values(dropdowns).forEach(dropdown => dropdown.classList.remove("show"));
        enableScroll();
    });

    megaContainer.addEventListener("mouseleave", function () {
        megaContainer.classList.remove("show");
        Object.values(dropdowns).forEach(dropdown => dropdown.classList.remove("show"));
        enableScroll();
    });

    const mainView = document.getElementById("womenMainCategories");

    document.querySelectorAll(".category-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const category = e.target.getAttribute("data-category");

            document.querySelectorAll(".category-view").forEach(view => view.classList.remove("active"));

            const sub = document.getElementById(`${category}Subcategories`);
            if (sub) sub.classList.add("active");
        });
    });

    document.querySelectorAll(".back-button").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            document.querySelectorAll(".category-view").forEach(view => view.classList.remove("active"));

            mainView.classList.add("active");
        });
    });
});
