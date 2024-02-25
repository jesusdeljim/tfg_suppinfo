document.addEventListener('DOMContentLoaded', function() {
  var menuIcon = document.querySelector('.menu-icon');
  var categoriesMenu = document.getElementById('categoriesMenu');

  menuIcon.addEventListener('click', function() {
    if (categoriesMenu.classList.contains('visible')) {
      categoriesMenu.classList.remove('visible');
    } else {
      categoriesMenu.classList.add('visible');
    }
  });
});