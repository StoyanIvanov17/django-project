// document.addEventListener("DOMContentLoaded", function() {
//     var minRange = document.getElementById("min-range");
//     var maxRange = document.getElementById("max-range");
//     var minValue = document.getElementById("min-value");
//     var maxValue = document.getElementById("max-value");
//
//     minRange.addEventListener("input", function() {
//         minValue.textContent = parseFloat(minRange.value).toFixed(2);
//         if (parseFloat(minRange.value) > parseFloat(maxRange.value)) {
//             minRange.value = maxRange.value;
//             minValue.textContent = parseFloat(maxRange.value).toFixed(2);
//         }
//     });
//
//     maxRange.addEventListener("input", function() {
//         maxValue.textContent = parseFloat(maxRange.value).toFixed(2);
//         if (parseFloat(maxRange.value) < parseFloat(minRange.value)) {
//             maxRange.value = minRange.value;
//             maxValue.textContent = parseFloat(minRange.value).toFixed(2);
//         }
//     });
//
//     minRange.addEventListener("change", applyFilter);
//     maxRange.addEventListener("change", applyFilter);
//
//     function applyFilter() {
//         var searchParams = new URLSearchParams(window.location.search);
//         searchParams.set("min_price", minRange.value);
//         searchParams.set("max_price", maxRange.value);
//         window.location.search = searchParams.toString();
//     }
// });
