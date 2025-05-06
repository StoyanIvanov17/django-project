document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.getElementById("main-product-image");
    const modal = document.getElementById("zoomImageModal");
    const modalImg = document.getElementById("zoomedImage");
    const closeBtn = document.querySelector("#zoomImageModal .close");

    function openModal() {
        modal.style.display = "block";
        modalImg.src = mainImage.src;
        document.body.style.overflow = "hidden";
    }

    function closeModal() {
        modal.style.display = "none";
        document.body.style.overflow = "";
    }

    if (mainImage && modal && modalImg && closeBtn) {
        mainImage.onclick = openModal;
        closeBtn.onclick = closeModal;

        window.onclick = function (event) {
            if (event.target === modal) {
                closeModal();
            }
        };
    }
});
