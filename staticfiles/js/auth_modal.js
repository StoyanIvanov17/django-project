document.addEventListener("DOMContentLoaded", function () {

    const userIcon = document.getElementById("userIcon");

    const authModal = document.getElementById("authModal");
    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    const authCloseBtn = document.getElementById("authCloseBtn");
    const loginCloseBtn = document.getElementById("loginCloseBtn");
    const registerCloseBtn = document.getElementById("registerCloseBtn");

    const emailCheckForm = document.getElementById("emailCheckForm");

    const authEmailInput = document.getElementById("authEmail");
    const loginEmailInput = document.getElementById("loginEmailInput");
    const registerEmailInput = document.getElementById("registerEmailInput");

    const isAuthenticated =
        document.body.dataset.authenticated === "true";

    const openRegisterModal =
        document.body.dataset.openRegisterModal === "true";

    const openLoginModal =
        document.body.dataset.openLoginModal === "true";

    function openModal(modal) {
        modal.style.display = "flex";
        document.body.classList.add("modal-open");
    }

    function closeModal(modal) {
        modal.style.display = "none";

        const anyOpen = [authModal, loginModal, registerModal]
            .some(m => m.style.display === "flex");

        if (!anyOpen) {
            document.body.classList.remove("modal-open");
        }
    }

    if (!userIcon) {
        return;
    }

    userIcon.addEventListener("click", function () {

        if (isAuthenticated) {
            window.location.href = "/accounts/profile/";
        } else {
            openModal(authModal);
        }
});

    authCloseBtn.addEventListener("click", function () {
        closeModal(authModal);
    });

    loginCloseBtn.addEventListener("click", function () {
        closeModal(loginModal);
    });

    registerCloseBtn.addEventListener("click", function () {
        closeModal(registerModal);
    });

    window.addEventListener("click", function (e) {

        if (e.target === authModal) {
            closeModal(authModal);
        }

        if (e.target === loginModal) {
            closeModal(loginModal);
        }

        if (e.target === registerModal) {
            closeModal(registerModal);
        }
    });

    emailCheckForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const email = authEmailInput.value;

        const csrfToken =
            document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/accounts/check-email/', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },

            body: `email=${encodeURIComponent(email)}`
        })

        .then(response => response.json())

        .then(data => {

            closeModal(authModal);

            if (data.exists) {
                loginEmailInput.value = email;
                openModal(loginModal);

            } else {
                registerEmailInput.value = email;
                openModal(registerModal);
            }
        })

        .catch(error => {
            console.error('Error:', error);
        });
    });

    const backToLoginFromRegister =
        document.getElementById("backToLoginFromRegister");

    if (backToLoginFromRegister) {

        backToLoginFromRegister.addEventListener("click", function () {

            closeModal(registerModal);
            openModal(authModal);
        });
    }

    const backToLoginFromLogin =
        document.getElementById("backToLoginFromLogin");

    if (backToLoginFromLogin) {

        backToLoginFromLogin.addEventListener("click", function () {

            closeModal(loginModal);
            openModal(authModal);
        });
    }

    if (openRegisterModal) {
        openModal(registerModal);
    }

    if (openLoginModal) {
        openModal(loginModal);
    }
});