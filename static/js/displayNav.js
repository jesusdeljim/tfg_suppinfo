document.addEventListener('DOMContentLoaded', function() {
    var menuIcon = document.querySelector('.menu-icon');
    var categoriesMenu = document.getElementById('categoriesMenu');
  
    menuIcon.addEventListener('click', function() {
      if (categoriesMenu.style.display === 'none' || categoriesMenu.style.display === '') {
        categoriesMenu.style.display = 'block';
      } else {
        categoriesMenu.style.display = 'none';
      }
    });
  });