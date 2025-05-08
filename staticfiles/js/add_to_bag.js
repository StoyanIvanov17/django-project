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

    const formData = new FormData(this);

    fetch(this.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
      },
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        document.getElementById('bag-modal-product-image').src = data.product_image_url;
        document.querySelector('.bag-modal-product-title').textContent = data.product_title;
        document.querySelector('.bag-modal-product-size').textContent = `Size: ${data.product_size}`;
        document.querySelector('.bag-modal-product-price').textContent = `BGN: ${data.price}`;

        const bagLink = document.getElementById('view-bag-link');
        const checkoutLink = document.getElementById('checkout-link');

        if (bagLink) bagLink.href = bagLink.dataset.url;
        if (checkoutLink) checkoutLink.href = checkoutLink.dataset.url;

        const modal = document.getElementById('bag-modal');
        modal.classList.remove('hidden');

        const closeModal = () => {
          modal.classList.add('hidden');
        };

        if (bagLink) bagLink.addEventListener('click', closeModal);
        if (checkoutLink) checkoutLink.addEventListener('click', closeModal);

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
