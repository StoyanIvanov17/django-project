document.addEventListener("DOMContentLoaded", function() {
    const button = document.querySelector(".test-button");
    const box = document.getElementById("something");

    button.addEventListener("mouseenter", function() {
        box.classList.remove("hidden");
    });

    button.addEventListener("mouseleave", function() {
        box.classList.add("hidden");
    });
})

