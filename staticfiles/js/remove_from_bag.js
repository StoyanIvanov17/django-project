document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.remove-from-bag-form');

    for (let i = 0; i < forms.length; i++) {
        const form = forms[i];

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
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const itemRow = form.closest('.bag-item');
                    if (!itemRow) return;

                    const quantitySpan = itemRow.querySelector('.item-quantity');
                    if (quantitySpan) {
                        if (data.quantity > 0) {
                            quantitySpan.textContent = data.quantity;
                        } else {
                            itemRow.remove();
                        }
                    }
                }
            })
            .catch(error => console.error('Error removing item:', error));
        });
    }
});
