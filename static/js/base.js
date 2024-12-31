// Toggle the visibility of the navbar menu
function toggleMenu() {
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');
    const navbarMenu = document.querySelector('.navbar-menu');

    if (menuIcon && closeIcon && navbarMenu) {
        menuIcon.classList.toggle('hidden');
        closeIcon.classList.toggle('hidden');
        navbarMenu.classList.toggle('active');
    }
}

// Toggle the visibility of the search form
function toggleSearch() {
    const searchIcon = document.getElementById('search-icon');
    const searchForm = document.querySelector('.search-form');

    if (searchIcon && searchForm) {
        searchForm.classList.toggle('active');

        if (searchForm.classList.contains('active')) {
            searchForm.querySelector('.search-input').focus();
        }
    }
}


// Toggle the visibility of the Profile dropdown menu
function toggleDropdown() {
    const dropdownMenu = document.getElementById('dropdown-menu');
    if (dropdownMenu) {
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    }
}

// Close dropdown menu if clicked outside
document.addEventListener('click', function (e) {
    const dropdownMenu = document.getElementById('dropdown-menu');
    const isDropdownClicked = e.target.closest('.profile-dropdown');
    if (!isDropdownClicked && dropdownMenu) {
        dropdownMenu.style.display = 'none';
    }
});
