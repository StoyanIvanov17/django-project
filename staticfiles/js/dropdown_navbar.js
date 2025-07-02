document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav-links a");
    const megaContainer = document.querySelector(".mega-dropdown-container");
    const dropdowns = {
        "WOMEN": document.getElementById("womenDropdown"),
        "MEN": document.getElementById("menDropdown"),
        "KIDS": document.getElementById("kidsDropdown")
    };

    navLinks.forEach(link => {
        const dropdownType = link.getAttribute("data-dropdown");
        if (dropdowns[dropdownType]) {
            link.addEventListener("mouseenter", function () {
                if (megaContainer) {
                    megaContainer.classList.add("show");
                }

                for (let key in dropdowns) {
                    if (dropdowns[key]) {
                        if (key === dropdownType) {
                            dropdowns[key].classList.add("show");
                        } else {
                            dropdowns[key].classList.remove("show");
                        }
                    }
                }
            });
        } else {
            console.log(`No matching dropdown for ${dropdownType}`);
        }
    });

    if (megaContainer) {
        megaContainer.addEventListener("mouseleave", () => {
            megaContainer.classList.remove("show");
            for (let key in dropdowns) {
                if (dropdowns[key]) {
                    dropdowns[key].classList.remove("show");
                }
            }
        });
    }
});
