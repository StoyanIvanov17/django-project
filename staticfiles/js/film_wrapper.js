document.addEventListener('DOMContentLoaded', function () {
    const film = document.querySelector('.new-arrivals-film-wrapper');

    if (!film) {
        return;
    }

    film.addEventListener('wheel', function (e) {
        if (e.deltaY === 0) return;

        e.preventDefault();
        film.scrollLeft += Number(e.deltaY);
    }, { passive: false });
});
