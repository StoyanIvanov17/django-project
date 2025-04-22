document.addEventListener("DOMContentLoaded", function () {
    const userIcon = document.getElementById("userIcon");
    const authModal = document.getElementById("authModal");
    const authCloseBtn = document.getElementById("authCloseBtn");
    const emailCheckForm = document.getElementById("emailCheckForm");
    const authEmailInput = document.getElementById("authEmail");

    userIcon.addEventListener("click", function () {
        authModal.style.display = "flex";
    });

    authCloseBtn.addEventListener("click", function () {
        authModal.style.display = "none";
    });

    window.addEventListener("click", function (e) {
        if (e.target === authModal) {
            authModal.style.display = "none";
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
            if (data.exists) {
                alert('Email exists! You can proceed with login.');
            } else {
                alert('Email does not exist! You can proceed with registration.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while checking the email.');
        });
    })
});
