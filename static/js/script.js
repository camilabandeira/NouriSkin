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
