function toggleMenu() {
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');
    const navbarMenu = document.querySelector('.navbar-menu');

    // Toggle visibility of icons
    menuIcon.classList.toggle('hidden');
    closeIcon.classList.toggle('hidden');

    // Toggle visibility of the menu
    navbarMenu.classList.toggle('active');
}

// Toggle the visibility of the search form
const searchIcon = document.getElementById('search-icon');
const searchForm = document.querySelector('.search-form');


searchIcon.addEventListener('click', () => {
    searchForm.classList.toggle('active');
});

searchIcon.addEventListener('click', () => {
    if (searchForm.classList.contains('active')) {
        searchForm.querySelector('.search-input').focus();
    }
});