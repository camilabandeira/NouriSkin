document.addEventListener('DOMContentLoaded', () => {
    const filterToggleBtn = document.getElementById('filter-toggle');
    const filterPopup = document.getElementById('filter-popup');
    const sidebarContent = document.querySelector('.products-sidebar');
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

    const createCloseButton = () => {
        const closePopupBtn = document.createElement('button');
        closePopupBtn.id = 'close-popup';
        closePopupBtn.className = 'close-popup-btn';
        closePopupBtn.textContent = '×';
        closePopupBtn.addEventListener('click', hidePopup);
        filterPopup.appendChild(closePopupBtn);
    };

    if (!document.getElementById('close-popup')) {
        createCloseButton();
    }
});
