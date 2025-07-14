document.addEventListener("DOMContentLoaded", function() {
    const minRange = document.getElementById("min-range");
    const maxRange = document.getElementById("max-range");
    const minValue = document.getElementById("min-value");
    const maxValue = document.getElementById("max-value");
    const sliderRange = document.querySelector(".slider-range");

    function updateRange() {
        const min = parseFloat(minRange.min);
        const max = parseFloat(maxRange.max);
        const minVal = parseFloat(minRange.value);
        const maxVal = parseFloat(maxRange.value);

        const percentMin = ((minVal - min) / (max - min)) * 100;
        const percentMax = ((maxVal - min) / (max - min)) * 100;

        sliderRange.style.left = percentMin + "%";
        sliderRange.style.width = (percentMax - percentMin) + "%";
    }

    if (!minRange) return;
    minRange.addEventListener("input", function() {
        minValue.textContent = parseFloat(minRange.value).toFixed(2);

        if (parseFloat(minRange.value) > parseFloat(maxRange.value)) {
            minRange.value = maxRange.value;
            minValue.textContent = parseFloat(maxRange.value).toFixed(2);
        }
        updateRange();
    });

    maxRange.addEventListener("input", function() {
        maxValue.textContent = parseFloat(maxRange.value).toFixed(2);

        if (parseFloat(maxRange.value) < parseFloat(minRange.value)) {
            maxRange.value = minRange.value;
            maxValue.textContent = parseFloat(minRange.value).toFixed(2);
        }
        updateRange();
    });

    minRange.addEventListener("change", applyFilter);
    maxRange.addEventListener("change", applyFilter);

    function applyFilter() {
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set("min_price", minRange.value);
        searchParams.set("max_price", maxRange.value);
        window.location.search = searchParams.toString();
    }

    minValue.textContent = parseFloat(minRange.value).toFixed(2);
    maxValue.textContent = parseFloat(maxRange.value).toFixed(2);
    updateRange();
});
