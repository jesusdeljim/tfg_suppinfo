document.addEventListener('DOMContentLoaded', function() {
    var flechaIzquierda = document.querySelector('.carrusel-flecha-izquierda');
    var flechaDerecha = document.querySelector('.carrusel-flecha-derecha');
    var contenedorProductos = document.querySelector('.productos-recomendados-card');
    var anchoProducto = document.querySelector('.producto-recomendado').clientWidth;
  
    flechaIzquierda.addEventListener('click', function() {
      // Desplaza el contenedor hacia la izquierda
      contenedorProductos.scrollBy({ left: -anchoProducto * 5, behavior: 'smooth' });
    });
  
    flechaDerecha.addEventListener('click', function() {
      // Desplaza el contenedor hacia la derecha
      contenedorProductos.scrollBy({ left: anchoProducto * 5, behavior: 'smooth' });
    });
  });