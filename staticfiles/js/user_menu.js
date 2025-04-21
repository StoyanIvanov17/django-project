document.addEventListener('DOMContentLoaded', function() {
    const userIcon = document.getElementById('userIcon');
    const userDropdown = document.getElementById('userDropdown');

    userIcon.addEventListener('click', function (e) {
    e.preventDefault();
    userDropdown.style.display =
      userDropdown.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', function (e) {
    if (!e.target.closest('.user-menu-container')) {
      userDropdown.style.display = 'none';
    }
    });
})