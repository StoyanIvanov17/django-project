document.addEventListener("DOMContentLoaded", function () {
    const userIcon = document.getElementById("userIcon");
    const authModal = document.getElementById("authModal");
    const authCloseBtn = document.getElementById("authCloseBtn");
    const loginCloseBtn = document.getElementById("loginCloseBtn");
    const registerCloseBtn = document.getElementById("registerCloseBtn");
    const emailCheckForm = document.getElementById("emailCheckForm");
    const authEmailInput = document.getElementById("authEmail");

    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");
    const loginEmailInput = document.getElementById("loginEmailInput");
    const registerEmailInput = document.getElementById("registerEmailInput");

    userIcon.addEventListener("click", function () {
        openModal(authModal);
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

    function openModal(modal) {
        modal.style.display = "flex";
        document.body.classList.add("modal-open");
    }

    function closeModal(modal) {
        modal.style.display = "none";

        const anyOpen = [authModal, loginModal, registerModal].some(m => m.style.display === "flex");
        if (!anyOpen) {
            document.body.classList.remove("modal-open");
        }
    }


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
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
                openModal(loginModal)
            } else {
                registerEmailInput.value = email;
                openModal(registerModal)
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while checking the email.');
        });
    });
    const backToLoginBtn = document.getElementById("backToLoginBtn");
    const backToLoginFromRegister = document.getElementById("backToLoginFromRegister");
    if (backToLoginFromRegister) {
        backToLoginFromRegister.addEventListener("click", function () {
            closeModal(registerModal);
            openModal(loginModal);
        });
    }

    const backToLoginFromLogin = document.getElementById("backToLoginFromLogin");
    if (backToLoginFromLogin) {
        backToLoginFromLogin.addEventListener("click", function () {
            closeModal(loginModal);
            openModal(authModal);
        });
    }
});
