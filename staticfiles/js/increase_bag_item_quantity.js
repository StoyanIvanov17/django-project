document.addEventListener('DOMContentLoaded', function () {
    const incForms = document.querySelectorAll('.increase-bag-item-quantity-form');

    for (let i = 0; i < incForms.length; i++) {
        const form = incForms[i];

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
                body: formData
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (!data.success) return;

                const itemRow = form.closest('.bag-item');
                if (!itemRow) return;

                const quantitySpan = itemRow.querySelector('.item-quantity');
                if (quantitySpan) quantitySpan.textContent = data.quantity;

                const bagCounter = document.querySelector('.bag-counter');
                if (bagCounter) bagCounter.textContent = data.bag_size;
            })
            .catch(function (err) {
                console.error('Error increasing item:', err);
            });
        });
    }
});
