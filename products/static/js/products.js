document.addEventListener("DOMContentLoaded", function () {
    const filterToggleBtn = document.getElementById('filter-toggle');
    const filterPopup = document.getElementById('filter-popup');
    const sidebarContent = document.querySelector('.products-sidebar');

    if (filterToggleBtn && filterPopup && sidebarContent) {
        const popupContent = filterPopup.querySelector('.popup-content');

        const showPopup = () => {
            filterPopup.style.display = 'block';
            setTimeout(() => {
                filterPopup.style.transform = 'translateX(0)';
            }, 10);
            popupContent.innerHTML = sidebarContent.innerHTML;
        };

        const hidePopup = () => {
            filterPopup.style.transform = 'translateX(-100%)';
            setTimeout(() => {
                filterPopup.style.display = 'none';
            }, 400);
        };

        filterToggleBtn.addEventListener('click', showPopup);
        filterPopup.addEventListener('transitionend', () => {
            if (filterPopup.style.transform === 'translateX(-100%)') {
                filterPopup.style.display = 'none';
            }
        });
    }

    const toggleButtons = document.querySelectorAll('.plus-minus-btn');

    if (toggleButtons.length > 0) {
        toggleButtons.forEach(button => {
            button.addEventListener('click', function () {
                const content = this.nextElementSibling;
                if (content && content.classList.contains('content-toggle')) {
                    const isVisible = content.style.display === 'block';
                    content.style.display = isVisible ? 'none' : 'block';
                    this.textContent = isVisible ? '+' : '−';
                }
            });
        });
    }

    const stars = document.querySelectorAll(".rating .fa");
    const form = document.querySelector("form");
    const ratingInput = document.getElementById("rating");
    const selectedRatingText = document.getElementById("selected-rating");

    stars.forEach((star) => {
        star.addEventListener("click", () => {
            const ratingValue = star.getAttribute("data-value");
            ratingInput.value = ratingValue;
            selectedRatingText.textContent = ratingValue;

            stars.forEach((s) => {
                s.classList.remove("fa-star");
                s.classList.add("fa-star-o");
            });

            for (let i = 0; i < ratingValue; i++) {
                stars[i].classList.remove("fa-star-o");
                stars[i].classList.add("fa-star");
            }
        });
    });

    form.addEventListener("submit", function (event) {
        if (!ratingInput.value || parseInt(ratingInput.value) === 0) {
            event.preventDefault();
            alert("Please select a star rating before submitting!");
        }
    });
});
