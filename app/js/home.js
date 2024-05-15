document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.hamburger').addEventListener('click', function() {
        document.querySelector('.wrapper').classList.toggle('collapse');
    });
});