document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.remove-from-bag-form');

    for (let i = 0; i < forms.length; i++) {
        const form = forms[i];

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
            .then(r => r.json())
            .then(data => {
                if (!data.success) return;

                const itemRow = form.closest('.bag-item');
                if (!itemRow) return;

                if (data.quantity > 0) {
                    const quantitySpan = itemRow.querySelector('.item-quantity');
                    if (quantitySpan) quantitySpan.textContent = data.quantity;
                } else {
                    itemRow.remove();
                }

                const bagCounter = document.querySelector('.bag-counter');
                if (bagCounter) bagCounter.textContent = data.bag_size;
            });
        });
    }
});
