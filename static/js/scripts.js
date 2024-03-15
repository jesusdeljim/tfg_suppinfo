document.addEventListener('DOMContentLoaded', function() {
  var menuIcon = document.querySelector('.menu-icon');
  var categoriesMenu = document.getElementById('categoriesMenu');

  menuIcon.addEventListener('click', function() {
    // Encuentra el ícono dentro del toggle
    var icon = menuIcon.querySelector('i');

    // Alternar la visibilidad del menú y la clase del ícono
    if (categoriesMenu.classList.contains('visible')) {
      categoriesMenu.classList.remove('visible');
      icon.classList.remove('fa-chevron-up');
      icon.classList.add('fa-chevron-down');
    } else {
      categoriesMenu.classList.add('visible');
      icon.classList.remove('fa-chevron-down');
      icon.classList.add('fa-chevron-up');
    }
  });
});

function toggleUserProfileNav() {
  var userProfileNav = document.getElementById("userProfileNav");
  if (userProfileNav.style.width === '250px') {
    userProfileNav.style.width = '0';
  } else {
    userProfileNav.style.width = '250px';
  }
}

function toggleEditProfile() {
  var csrftoken = $('meta[name="csrf-token"]').attr('content'); // Obtiene el token CSRF

  $('#edit-profile-details').hide();
  
  $('div.user-details').wrap('<form method="post" enctype="multipart/form-data" class="user-details" id="editProfileForm"></form>');
  $('#editProfileForm').prepend('<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">');
  
  if ($('input[type="file"][name="profile_image"]').length === 0) {
    $('form').append('<input type="file" name="profile_image" accept="image/*">');
  }
  $('p.user-detail-field').each(function(){
    var content = $(this).text().trim();
    var name = $(this).attr('name');
    if(name === "fecha_nacimiento") {
      var months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
      var date = content.split(" ");
      var formattedDate = date[4] + "-" + (months.indexOf(date[2]) + 1).toString().padStart(2, '0') + "-" + date[0];
      console.log(formattedDate);
      $(this).replaceWith('<input type="date" name="'+name+'" value="' + formattedDate + '">');
    } else {
      $(this).replaceWith('<textarea name="'+name+'">' + content + '</textarea>');
    }
  });
  
  $('#save-profile-details').show();
  $('#cancel-profile-details').show();
}

function cancelEditProfile() {
  $('#save-profile-details').hide();
  $('#cancel-profile-details').hide();
  $('#edit-profile-details').show();
  $('#editProfileForm input[type="date"]').each(function() {
    var value = $(this).val();
    var name = $(this).attr('name');
    $(this).replaceWith($('<p id="editProfileForm" class="user-detail-field" name="'+name+'"></p>').text(value));
  }
  );
  $('#editProfileForm input[type="file"]').each(function() {
    $(this).remove();
  }
  );
  $('#editProfileForm textarea').each(function() {
    var value = $(this).val();
    var name = $(this).attr('name');
    $(this).replaceWith($('<p id="editProfileForm" class="user-detail-field" name="'+name+'"></p>').text(value));
  });
  $('form#editProfileForm').contents().unwrap();
}

function saveProfileDetails() {
  var fechaActual = new Date();
  var fechaMinima = new Date(fechaActual.getFullYear() - 18, fechaActual.getMonth(), fechaActual.getDate());

  var fechaNacimientoInput = $('#editProfileForm input[name="fecha_nacimiento"]');
  var fechaNacimiento = new Date(fechaNacimientoInput.val());

  if (isNaN(fechaNacimiento.getTime()) || fechaNacimiento > fechaMinima) {
    alert('Debes tener al menos 18 años de edad.');
    return;
  }

  // Crea un objeto FormData para enviar los datos del formulario, incluida la imagen
  var formData = new FormData($('#editProfileForm')[0]);

  $.ajax({
    url: '/save_profile_data/', 
    method: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
      // Aquí manejas una respuesta exitosa del servidor
      $('#save-profile-details').hide();
      $('#edit-profile-details').show();
      $('#cancel-profile-details').hide();
      // Convierte los textarea de nuevo a texto
      if(response.profile_image_url) {
        $('.user-profile-picture').attr('src', response.profile_image_url);
      }
      $('#editProfileForm input').each(function() {
        if($(this).attr('type') === 'date') {
          var value = $(this).val();
          var name = $(this).attr('name');
          $(this).replaceWith($('<p id="editProfileForm" class="user-detail-field" name="'+name+'"></p>').text(value));
        } else if($(this).attr('type') === 'file') {
          $(this).remove();
        }
        else {
          //do nothing
        }    
      });
      $('#editProfileForm textarea').each(function() {
        var value = $(this).val();
        var name = $(this).attr('name');
        $(this).replaceWith($('<p id="editProfileForm" class="user-detail-field" name="'+name+'"></p>').text(value));
      });
      $('form#editProfileForm').contents().unwrap();
    },
    error: function() {
      // Aquí manejas errores
      alert('Hubo un error al guardar los cambios.');
    }
  });
}


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
function showAdvancedSearch() {
  document.getElementById('advanced-search-btn').style.display = 'block';
  
}

function toggleAdvancedSearch() {
  var advancedSearchContainer = document.getElementById('advanced-search-container');
  var isDisplayed = advancedSearchContainer.style.display !== 'none';
  advancedSearchContainer.style.display = isDisplayed ? 'none' : 'flex';
}

//si el elemento advanced-search-container tiene display: flex, quiero que hacer click fuera de él lo oculte
document.addEventListener('click', function(event) {
  var advancedSearchContainer = document.getElementById('advanced-search-container');
  var advancedSearchBtn = document.getElementById('advanced-search-btn');
  var searchInput = document.getElementById('search-input');
  if (!advancedSearchContainer.contains(event.target) & !advancedSearchBtn.contains(event.target) & !searchInput.contains(event.target) & event.target !== advancedSearchContainer) {
    advancedSearchContainer.style.display = 'none';
    advancedSearchBtn.style.display = 'none';
  }
});

document.addEventListener('DOMContentLoaded', function () {
  var priceRangeSlider = document.getElementById('price-range-slider');
  var priceRangeLabel = document.getElementById('price-range-label');
  if (priceRangeSlider) {
    noUiSlider.create(priceRangeSlider, {
      start: [0, 200],
      connect: true,
      range: {
        'min': 0,
        'max': 200
      },
      format: {
        to: function (value) {
          return value.toFixed(0) + '€';
        },
        from: function (value) {
          return Number(value.replace('€', ''));
        }
      }
    });

    priceRangeSlider.noUiSlider.on('update', function (values, handle) {
      priceRangeLabel.innerHTML = values.join(' - ');
    });
  }
});

function performAdvancedSearch() {
  var priceRange = document.getElementById('price-range-label').innerHTML;
  var productName = document.getElementById('advanced-search-name').value;
  var minRating = document.getElementById('advanced-search-rating').value;
  var inStock = document.getElementById('advanced-search-stock').checked;
  var keywords = document.getElementById('advanced-search-keywords').value;
  var brand = document.getElementById('advanced-search-brand').value;
  var ingredients = document.getElementById('advanced-search-ingredients').value;
  var flavor = document.getElementById('advanced-search-flavor').value;
  // Make the logic to send the request to the server
  var searchURL = '/advanced_search/?';

  if (productName.trim() !== '') {
    searchURL += 'name=' + encodeURIComponent(productName) + '&';
  }
  if (minRating.trim() !== '') {
    searchURL += 'rating=' + encodeURIComponent(minRating) + '&';
  }
  if (inStock) {
    searchURL += 'stock=' + encodeURIComponent(inStock) + '&';
  }
  if (keywords.trim() !== '') {
    searchURL += 'keywords=' + encodeURIComponent(keywords) + '&';
  }
  if (brand.trim() !== '') {
    searchURL += 'brand=' + encodeURIComponent(brand) + '&';
  }
  if (ingredients.trim() !== '') {
    searchURL += 'ingredients=' + encodeURIComponent(ingredients) + '&';
  }
  if (flavor.trim() !== '') {
    searchURL += 'flavor=' + encodeURIComponent(flavor) + '&';
  }
  if (priceRange !== '0 - 999') {
    var priceRangeValues = priceRange.split(' - ');
    searchURL += 'min_price=' + priceRangeValues[0].replace('€', '') +
                 '&max_price=' + priceRangeValues[1].replace('€', '') + '&';
  }

  // Remove the trailing '&' if there are no additional parameters
  if (searchURL.endsWith('&')) {
    searchURL = searchURL.slice(0, -1);
  }

  // Redirige a la página de búsqueda con los parámetros adecuados
  window.location.href = searchURL;
  
  document.getElementById('advanced-search-btn').style.display = 'none';
  document.getElementById('advanced-search-container').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
  var flechaIzquierda = document.querySelector('.carrusel-flecha-izquierda');
  var flechaDerecha = document.querySelector('.carrusel-flecha-derecha');
  var contenedorProductos = document.querySelector('.productos-recomendados-card');
  var anchoProducto = document.querySelector('.producto-recomendado').clientWidth;

  flechaIzquierda.addEventListener('click', function() {
    // Desplaza el contenedor hacia la izquierda
    contenedorProductos.scrollBy({ left: -anchoProducto * 4, behavior: 'smooth' });
  });

  flechaDerecha.addEventListener('click', function() {
    // Desplaza el contenedor hacia la derecha
    contenedorProductos.scrollBy({ left: anchoProducto * 4, behavior: 'smooth' });
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

function orderProducts(orderBy) {
  // Construye la URL con el parámetro de ordenación
  const url = new URL(window.location);
  url.searchParams.set('order', orderBy);
  
  // Redirige a la URL con el parámetro de ordenación
  window.location.href = url.href;
}