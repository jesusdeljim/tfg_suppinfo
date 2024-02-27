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

document.addEventListener('DOMContentLoaded', function() {
  // Agrega un detector de eventos al documento
  document.addEventListener('click', function(event) {
    var searchResultsContainer = document.getElementById('search-results');
    var searchInput = document.getElementById('search-input');

    // Verifica si el clic fue fuera del contenedor de resultados y del campo de búsqueda
    if (!searchResultsContainer.contains(event.target) && event.target !== searchInput) {
      searchResultsContainer.style.display = 'none'; // Oculta los resultados
    }
  });
});

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

function searchProducts() {
    var searchTerm = document.getElementById('search-input').value;
    var searchResultsContainer = document.getElementById('search-results');
  
    if (searchTerm.trim() !== '') {
      fetch('/search/?query=' + encodeURIComponent(searchTerm))
        .then(response => response.json())
        .then(data => {
          searchResultsContainer.innerHTML = '';
          searchResultsContainer.style.display = 'block';

        // Muestra los productos
        data.products.forEach(product => {
          var productLink = document.createElement('a');
          productLink.href = '/producto/' + product.id; // Asume que tienes una URL con el patrón /producto/{id}
          productLink.classList.add('search-result-item');

          var productImage = document.createElement('img');
          productImage.src = product.imagen.startsWith('/') ? product.imagen : '/' + product.imagen; // Asume que la respuesta tiene un campo 'imagen_url'
          productImage.alt = product.nombre; // Asume que la respuesta tiene un campo 'nombre'
          productImage.classList.add('search-result-image');

          var productName = document.createElement('span');
          productName.textContent = product.nombre;
          productName.classList.add('search-result-name');

          var productPrice = document.createElement('span');
          productPrice.textContent = product.precio + '€'; // Asume que la respuesta tiene un campo 'precio'
          productPrice.classList.add('search-result-price');

          productLink.appendChild(productImage);
          productLink.appendChild(productName);
          productLink.appendChild(productPrice); // Añade el precio al elemento del producto
          searchResultsContainer.appendChild(productLink);
        });

        // Muestra el número total de coincidencias si es mayor que 10
        if (data.total_matches > 10) {
          var matchesElement = document.createElement('div');
          matchesElement.classList.add('search-result-matches');
          matchesElement.textContent = 'Total coincidencias: ' + data.total_matches;
          searchResultsContainer.appendChild(matchesElement);
        }
      })
      .catch(error => {
        console.error('Error al realizar la búsqueda:', error);
      });
  } else {
    searchResultsContainer.innerHTML = '';
    searchResultsContainer.style.display = 'none'; // Oculta los resultados si el campo de búsqueda está vacío
  }
}