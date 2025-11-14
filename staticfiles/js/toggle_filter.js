document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggle-filter');
    const filterPanel = document.getElementById('filter-panel');
    const contentWrapper = document.getElementById('content-wrapper');

    if (!filterPanel) return;
    const items = filterPanel.children;

    function openFilter() {
        filterPanel.classList.add('open');
        contentWrapper.classList.add('shifted');
        toggleBtn.innerHTML = 'Hide Filters <i class="fa-solid fa-filter"></i>';
        for (let i = 0; i < items.length; i++) {
            items[i].style.transitionDelay = `${(i + 1) * 0.1}s`;
        }
    }

    function closeFilter() {
        filterPanel.classList.remove('open');
        contentWrapper.classList.remove('shifted');
        toggleBtn.innerHTML = 'Show Filters <i class="fa-solid fa-filter products-filter"></i>';
        for (let i = 0; i < items.length; i++) {
            items[i].style.transitionDelay = `0s`;
        }
    }

    if (sessionStorage.getItem('filterPanelOpen') === 'true') {
        openFilter();
    } else {
        closeFilter();
    }

    toggleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (filterPanel.classList.contains('open')) {
            closeFilter();
            sessionStorage.setItem('filterPanelOpen', 'false');
        } else {
            openFilter();
            sessionStorage.setItem('filterPanelOpen', 'true');
        }
    });

    document.querySelectorAll('.filter-title').forEach(title => {
        title.addEventListener('click', () => {
            const group = title.parentElement;
            const options = group.querySelector('.filter-options');

            if (group.classList.contains('open')) {
                options.style.maxHeight = options.scrollHeight + 'px';
                setTimeout(() => options.style.maxHeight = '0', 10);
                group.classList.remove('open');
            } else {
                group.classList.add('open');
                options.style.maxHeight = options.scrollHeight + 'px';
            }
        });
    });

    document.querySelectorAll('#filter-panel input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            this.closest('form').submit();
        });
    });
});
