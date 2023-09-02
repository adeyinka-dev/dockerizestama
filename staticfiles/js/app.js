window.addEventListener('resize', () => {
    const navbar = document.getElementById('navbar');
    const isMobile = window.innerWidth <= 767;

    if (isMobile) {
        navbar.classList.remove('sidebar');
        navbar.classList.add('navbar');
    } else {
        navbar.classList.remove('navbar');
        navbar.classList.add('sidebar');
    }
});

window.dispatchEvent(new Event('resize'));
