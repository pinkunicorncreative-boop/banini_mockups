document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNavOverlay = document.querySelector('.mobile-nav-overlay');
    const mobileMenuClose = document.querySelector('.mobile-menu-close');
    const navLinks = document.querySelectorAll('.mobile-nav-links a, .mobile-nav-action');

    const toggleMenu = () => {
        const isOpen = mobileNavOverlay.classList.toggle('open');
        mobileMenuToggle.classList.toggle('open', isOpen);
        document.body.classList.toggle('no-scroll', isOpen);
    };

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleMenu);
    }

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', toggleMenu);
    }

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (mobileNavOverlay.classList.contains('open')) {
                toggleMenu();
            }
        });
    });
});
