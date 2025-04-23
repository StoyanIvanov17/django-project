document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.getElementById("profileIcon");
    const profileModal = document.getElementById("profileModal");
    const profileCloseBtn = document.getElementById("profileCloseBtn");
    const logoutBtn = document.getElementById("logoutBtn");

    if (profileIcon) {
        profileIcon.addEventListener("click", function () {
            profileModal.style.display = "flex";
        });
    }

    profileCloseBtn.addEventListener("click", function () {
        profileModal.style.display = "none";
    });

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            fetch('/accounts/logout/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/';
                } else {
                    alert('Logout failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while logging out.');
            });
        });
    }
});
