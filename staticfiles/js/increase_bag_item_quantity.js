document.addEventListener('DOMContentLoaded', function () {
    const incForms = document.querySelectorAll('.increase-bag-item-quantity-form');

    for (let i = 0; i < incForms.length; i++) {
        const form = incForms[i];

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const data = {
                product_id: form.querySelector('[name=product_id]').value,
                size_id: form.querySelector('[name=size_id]').value,
            }

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify(data)
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
