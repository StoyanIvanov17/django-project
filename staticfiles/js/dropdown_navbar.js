document.addEventListener("DOMContentLoaded", function (){
    const navLinks = document.querySelectorAll(".nav-left a");
    const megaContainer = document.querySelector(".nav-dropdown-container");

    const dropdowns = {
        MENU: document.getElementById("menuDropdown"),
    };

    function closeAll() {
        megaContainer.classList.remove("show");

        for (let key in dropdowns) {
            if (dropdowns[key])
                dropdowns[key].classList.remove("show");
        }
    }

    navLinks.forEach(function (link) {
        const type = link.getAttribute("data-dropdown");
        const dropdown = dropdowns[type];

        if (!dropdown) return;

        link.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();

            const isOpen = dropdown.classList.contains("show");

            closeAll();

            if (!isOpen) {
                megaContainer.classList.add("show");
                dropdown.classList.add("show");
            }
        });
    });

    megaContainer.addEventListener("click", function (e) {
        e.stopPropagation();
    });

    document.addEventListener("click", function () {
        closeAll();
    });
});
