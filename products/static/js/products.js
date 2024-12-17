document.addEventListener('DOMContentLoaded', () => {
    // Filter Popup Logic
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

    // Plus/Minus Button Logic
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
});
