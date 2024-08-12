//main fie script
$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

function toggleMenu() {
    const menu = document.getElementById('iconMenu');
    menu.classList.toggle('active');
}

