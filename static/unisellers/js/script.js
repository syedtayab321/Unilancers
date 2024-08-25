//main fie script
$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

function toggleMenu() {
    const menu = document.getElementById('iconMenu');
    menu.classList.toggle('active');
}

// JavaScript for toggling mobile navbar
document.querySelector('.menu-icon').addEventListener('click', function() {
    const navbarLinks = document.querySelector('.navbar-links');
    navbarLinks.classList.toggle('active');
});
document.querySelectorAll('.testimonial-images img').forEach(img => {
    img.addEventListener('click', function() {
        document.querySelector('.testimonial-images img.active').classList.remove('active');
        this.classList.add('active');
        // Change testimonial content based on the selected image
        // You can customize this part as needed
    });
});
