document.addEventListener('DOMContentLoaded', function () {
  const pinpointData = window.pinpointData;

  const pinpoints = document.querySelectorAll('.pinpoint');
  const previewDiv = document.querySelector('.image-preview');

  pinpoints.forEach(pin => {
    pin.addEventListener('click', function(event) {
      event.preventDefault();

      const pinpointClass = Array.from(this.classList).find(cls => cls !== 'pinpoint');

      if (pinpointClass && pinpointData[pinpointClass]) {
        const { image, url, name, price } = pinpointData[pinpointClass];
        previewDiv.innerHTML = `
          <a href="${url}">
            <img src="${image}" alt="Preview Image">
          </a>
          <div class="product-info">
            <h3>${name}</h3>
            <p>€${price}</p>
            <a href="${url}" class="button">Discover</a>
          </div>
        `;
      }
    });

    pin.addEventListener('mouseenter', function() {
      pinpoints.forEach(p => p.classList.remove('pulsate'));
      this.classList.add('pulsate');
    });
  });

  const firstPinpoint = document.querySelector('.pinpoint.one');
  if (firstPinpoint) {
    firstPinpoint.classList.add('pulsate');
    firstPinpoint.click();
  }
});
