document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#addToBagForm');

    if (!form) return;

    const closeBagModal = () => {
        const modal = document.getElementById('bag-modal');

        if (modal) {
          modal.classList.add('hidden');
        }
    };

    form.addEventListener('submit', function (e) {
    e.preventDefault();

    const data = {
        product_id: form.querySelector('[name="product_id"]').value,
        size_id: form.querySelector('[name="size_id"]').value,
        quantity: form.querySelector('[name="quantity"]').value,
    };

    fetch(this.action, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      },
      body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Response data:', data);

            document.getElementById('bag-modal-product-image').src = data.bag_item.product.image_url;
            document.querySelector('.bag-modal-product-title').textContent = data.bag_item.product.title;
            document.querySelector('.bag-modal-product-size').textContent = `Size: ${data.bag_item.size.name}`;
            document.querySelector('.bag-modal-product-price').textContent = `BGN: ${data.bag_item.product.price}`;

            const bagLink = document.getElementById('view-bag-link');
            const checkoutLink = document.getElementById('checkout-link');

            if (bagLink) {
                bagLink.href = bagLink.dataset.url;
            }

            if (checkoutLink) {
                checkoutLink.href = checkoutLink.dataset.url;
            }

            const modal = document.getElementById('bag-modal');
            modal.classList.remove('hidden');

            if (modal) {
                modal.addEventListener('click', function (event) {
                    if (!modal.classList.contains('hidden') && event.target === modal) {
                        modal.classList.add('hidden');
                    }
                });
            }

            const closeModal = () => {
              modal.classList.add('hidden');
            };

            if (bagLink) {
                bagLink.addEventListener('click', closeModal);
            }

            if (checkoutLink) {
                checkoutLink.addEventListener('click', closeModal);
            }

            const bagSizeElement = document.getElementById('view-bag-link');
            bagSizeElement.innerText = 'View Bag (' + data.bag_size + ')'

            setTimeout(closeModal, 5000);
          })
          .catch(error => {
            console.error('Error adding product to bag:', error);
          });
    });

    const closeButton = document.querySelector('.bag-modal-close');

    if (closeButton) {
        closeButton.addEventListener('click', closeBagModal);
    }
});
