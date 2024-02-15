from ..utils.imports import *
from ..utils.utils import *

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url_raw = "https://getrawnutrition.com"

def raw_scrap_pre_workout(driver):    
    url_preworkout = str(url_raw)+"/collections/pre-workout"

    f = urllib.request.urlopen(url_preworkout)
    s = BeautifulSoup(f, "lxml")
    prewList = s.find("div", class_="filters-adjacent collection-listing").find_all("div", class_="block-inner-inner")
    subcategoria_scrapeada = s.find("h1", class_="overlay-text__title super-large-text").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    
    writer = ix.writer()
    for e in prewList:
        
        url = e.find("a")['href']
        f = urllib.request.urlopen(url_raw+str(url))
        s = BeautifulSoup(f, "lxml")
        
        nombre = s.find("div", class_="title-row").text

        marca = "RAW Nutrition"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        precio = s.find("div", class_="price-area").find("span").text.replace("$", "")

        rating = s.find("div", class_="loox-rating")['data-rating']
        
        descripcion = s.find("div", class_="product-description rte cf").find_all("p")
        descripcion_final = "".join(str(e.text) for e in descripcion)

        stock = True
        stock_div = s.find("div", class_="quantity-submit-row__submit input-row")
    
        if(stock_div == None):
            if(s.find("div", class_="lightly-spaced-row not-in-quickbuy")):
                stock = True
                nombre = nombre + " [EN STOCK A TRAVÉS DE OTRO VENDEDOR]"
            else:
                stock = False
        elif(stock_div.find("div", class_="product-unavailable")):
            stock = False
        else:
            stock = True
    
        ingredientes_aux = s.find("div", class_="collapsible-tabs").find_all("div", class_="collapsible-tabs__block")
        ingredientes = []
        for i in ingredientes_aux:
            ingredientes.append(i.find("summary").text)
        
        sabores_aux = s.find("div", class_="option-selector option-selector--swatch")
        sabores=[]
        if (sabores_aux != None):
            for s in sabores_aux.find_all("li"):
                sabores.append(s.text.strip())
        else:
            sabores.append("Sin sabor")

        url_producto = str(url_raw)+str(url)
        
        get_imagen_raw(url_raw+str(url), driver)

        reviews_list = get_reviews_raw(url_producto, driver)
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        #almacenamos en la BD
        
        lista_ingredientes = []
        lista_sabores = []
        
        for i in ingredientes:
            i = i.strip()
            ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente = i)[0]
            lista_ingredientes.append(ingrediente_obj)
        for s in sabores:
            s = s.strip()
            sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
            lista_sabores.append(sabor_obj)
        try:
            existe_registro = Producto.objects.filter(url=url_producto).exists()
            if not existe_registro:
                p = Producto.objects.create(nombre = nombre,
                                            marca = brand,
                                            precio = precio,
                                        categoria = categoria,
                                        subcategoria = subcategoria,
                                        stock = stock,
                                        url = url_producto,
                                        rating_original = rating,                                       
                                        )
                producto_id = p.id
                writer.add_document(id_producto = str(producto_id),nombre=nombre, descripcion=descripcion_final, reviews = reviews)
                with open('temp.jpg', 'rb') as imagen_file:
                            p.imagen.save("images/"+nombre.strip()+'.jpg', File(imagen_file), save=True)
                os.remove('temp.jpg')
                
                p.sabor.set(lista_sabores)
                p.ingrediente.set(lista_ingredientes)
                print(f"Registro introducido en la BD: {nombre}")
            else:
                print(f"Registro duplicado: {nombre}")
        except IntegrityError as e:
            print(f"Se ha producido un error: {e}")
            print(f"Error al guardar el registro: {nombre}")
        time.sleep(1)
    writer.commit()
    print("Se han cargado " +str(ix.searcher().doc_count()) + "descripciones y reviews")
    return Producto.objects.count()



def raw_scrap_protein(driver):
    url_protein = str(url_raw)+"/collections/protein"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    proteinList = s.find("div", class_="filters-adjacent collection-listing").find_all("div", class_="block-inner-inner")
    subcategoria_scrapeada = s.find("h1", class_="overlay-text__title super-large-text").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    writer = ix.writer()
    for p in proteinList:
        url = p.find("a")['href']
        try:
            f = urllib.request.urlopen(url_raw+str(url))

            s = BeautifulSoup(f, "lxml")
            nombre = s.find("div", class_="title-row").text
            marca = "RAW Nutrition"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            precio = s.find("div", class_="price-area").find("span").text.replace("$", "")

            rating = s.find("div", class_="loox-rating")['data-rating']
            
            descripcion = s.find("div", class_="product-description rte cf").find_all("p")
            descripcion_final = "".join(str(e.text) for e in descripcion)
            
            stock = True
            stock_div = s.find("div", class_="quantity-submit-row__submit input-row")
        
            if(stock_div == None):
                if(s.find("div", class_="lightly-spaced-row not-in-quickbuy")):
                    stock = True
                    nombre = nombre + " [EN STOCK A TRAVÉS DE OTRO VENDEDOR]"
                else:
                    stock = False
            elif(stock_div.find("div", class_="product-unavailable")):
                stock = False
            else:
                stock = True

            ingredientes_aux = s.find("div", class_="collapsible-tabs").find_all("div", class_="collapsible-tabs__block")
            ingredientes = []
            for i in ingredientes_aux:
                ingredientes.append(i.find("summary").text)
            sabores_aux = s.find("div", class_="option-selector option-selector--swatch")
            sabores=[]
            if (sabores_aux != None):
                for s in sabores_aux.find_all("li"):
                    sabores.append(s.text.strip())
            else:
                sabores.append("Sin sabor")
            url_producto = str(url_raw)+str(url)

            get_imagen_raw(url_raw+str(url), driver)

            reviews_list = get_reviews_raw(url_producto, driver)
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
        except HTTPError as e:
            if e.code == 404:
                # Manejar el error 404 aquí (por ejemplo, imprimir un mensaje)

                print(f"La URL {url_raw}{url} devolvió un error 404. Saltando a la siguiente iteración.")
            else:
                # Manejar otros códigos de error si es necesario

                print(f"Error {e.code} al abrir la URL {url_raw}{url}.")

            # Pasa a la siguiente iteración del bucle
            continue
        except Exception as e:
            # Manejar otros tipos de errores si es necesario

            print(f"Error al abrir la URL {url_raw}{url}: {e}")

            # Pasa a la siguiente iteración del bucle
            continue


        #almacenamos en la BD
        
        lista_ingredientes = []
        lista_sabores = []
        
        for i in ingredientes:
            i = i.strip()
            ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente = i)[0]
            lista_ingredientes.append(ingrediente_obj)
        for s in sabores:
            s = s.strip()
            sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
            lista_sabores.append(sabor_obj)
        try:
            existe_registro = Producto.objects.filter(url=url_producto).exists()
            if not existe_registro:
                p = Producto.objects.create(nombre = nombre,
                                            marca = brand,
                                            precio = precio,
                                        categoria = categoria,
                                        subcategoria = subcategoria,
                                        stock = stock,
                                        url = url_producto,
                                        rating_original = rating,
                                        )
                producto_id = p.id
                writer.add_document(id_producto = str(producto_id),nombre=nombre, descripcion=descripcion_final, reviews = reviews)
                with open('temp.jpg', 'rb') as imagen_file:
                            p.imagen.save("images/"+nombre.strip()+'.jpg', File(imagen_file), save=True)
                os.remove('temp.jpg')
                
                p.sabor.set(lista_sabores)
                p.ingrediente.set(lista_ingredientes)
                print(f"Registro introducido en la BD: {nombre}")
            else:
                print(f"Registro duplicado: {nombre}")
        except IntegrityError as e:
            print(f"Se ha producido un error: {e}")
            print(f"Error al guardar el registro: {nombre}")
        time.sleep(1)
    writer.commit()
    print("Se han cargado " +str(ix.searcher().doc_count()) + "descripciones y reviews")
    return Producto.objects.count()
    
def raw_scrap_intra(driver):

    url_intra = str(url_raw)+"/collections/pump"
    f = urllib.request.urlopen(url_intra)
    s = BeautifulSoup(f, "lxml")
    intraList = s.find("div", class_="filters-adjacent collection-listing").find_all("div", class_="block-inner-inner")
    subcategoria_scrapeada = s.find("h1", class_="overlay-text__title super-large-text").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    writer = ix.writer()
    for i in intraList:
        url = i.find("a")['href']
        f = urllib.request.urlopen(url_raw+str(url))
        s = BeautifulSoup(f, "lxml")
        nombre = s.find("div", class_="title-row").text
        marca = "RAW Nutrition"
        brand = Marca.objects.get_or_create(nombre = marca)[0]
        precio = s.find("div", class_="price-area").find("span").text.replace("$", "")
        rating = s.find("div", class_="loox-rating")['data-rating']
        
        descripcion = s.find("div", class_="product-description rte cf").find_all("p")
        descripcion_final = "".join(str(e.text) for e in descripcion)
        stock = True
        stock_div = s.find("div", class_="quantity-submit-row__submit input-row")
    
        if(stock_div == None):
            if(s.find("div", class_="lightly-spaced-row not-in-quickbuy")):
                stock = True
                nombre = nombre + " [EN STOCK A TRAVÉS DE OTRO VENDEDOR]"
            else:
                stock = False
        elif(stock_div.find("div", class_="product-unavailable")):
            stock = False
        else:
            stock = True

        ingredientes_aux = s.find("div", class_="collapsible-tabs").find_all("div", class_="collapsible-tabs__block")
        ingredientes = []
        for i in ingredientes_aux:
            ingredientes.append(i.find("summary").text)
        sabores_aux = s.find("div", class_="option-selector option-selector--swatch")
        sabores=[]
        if (sabores_aux != None):
            for s in sabores_aux.find_all("li"):
                sabores.append(s.text.strip())
        else:
            sabores.append("Sin sabor")
        url_producto = str(url_raw)+str(url)

        get_imagen_raw(url_raw+str(url), driver)

        reviews_list = get_reviews_raw(url_producto, driver)
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        #almacenamos en la BD
        
        lista_ingredientes = []
        lista_sabores = []
        
        for i in ingredientes:
            i = i.strip()
            ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente = i)[0]
            lista_ingredientes.append(ingrediente_obj)
        for s in sabores:
            s = s.strip()
            sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
            lista_sabores.append(sabor_obj)
        try:
            existe_registro = Producto.objects.filter(url=url_producto).exists()
            if not existe_registro:
                p = Producto.objects.create(nombre = nombre,
                                            marca = brand,
                                            precio = precio,
                                        categoria = categoria,
                                        subcategoria = subcategoria,
                                        stock = stock,
                                        url = url_producto,
                                        rating_original = rating,
                                        )
                producto_id = p.id
                writer.add_document(id_producto = str(producto_id),nombre=nombre, descripcion=descripcion_final, reviews = reviews)
                
                with open('temp.jpg', 'rb') as imagen_file:
                            p.imagen.save("images/"+nombre.strip()+'.jpg', File(imagen_file), save=True)
                os.remove('temp.jpg')
                
                p.sabor.set(lista_sabores)
                p.ingrediente.set(lista_ingredientes)
                print(f"Registro introducido en la BD: {nombre}")
            else:
                print(f"Registro duplicado: {nombre}")
        except IntegrityError as e:
            print(f"Se ha producido un error: {e}")
            print(f"Error al guardar el registro: {nombre}")
        time.sleep(1)
    writer.commit()
    print("Se han cargado " +str(ix.searcher().doc_count()) + "descripciones y reviews")
    return Producto.objects.count()
        

def raw_scrap_recovery(driver):
    url_recovery = str(url_raw)+"/collections/recovery"
    f = urllib.request.urlopen(url_recovery)
    s = BeautifulSoup(f, "lxml")
    recoveryList = s.find("div", class_="filters-adjacent collection-listing").find_all("div", class_="block-inner-inner")
    subcategoria_scrapeada = s.find("h1", class_="overlay-text__title super-large-text").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    writer = ix.writer()
    for r in recoveryList:
        url = r.find("a")['href']
        f = urllib.request.urlopen(url_raw+str(url))
        s = BeautifulSoup(f, "lxml")
        nombre = s.find("div", class_="title-row").text
        marca = "RAW Nutrition"
        brand = Marca.objects.get_or_create(nombre = marca)[0]
        precio = s.find("div", class_="price-area").find("span").text.replace("$", "")
        rating = s.find("div", class_="loox-rating")['data-rating']
        
        descripcion = s.find("div", class_="product-description rte cf").find_all("p")
        descripcion_final = "".join(str(e.text) for e in descripcion)
        stock = True
        stock_div = s.find("div", class_="quantity-submit-row__submit input-row")
    
        if(stock_div == None):
            if(s.find("div", class_="lightly-spaced-row not-in-quickbuy")):
                stock = True
                nombre = nombre + " [EN STOCK A TRAVÉS DE OTRO VENDEDOR]"
            else:
                stock = False
        elif(stock_div.find("div", class_="product-unavailable")):
            stock = False
        else:
            stock = True
        
        ingredientes_aux = s.find("div", class_="collapsible-tabs").find_all("div", class_="collapsible-tabs__block")
        ingredientes = []
        for i in ingredientes_aux:
            ingredientes.append(i.find("summary").text)
        sabores_aux = s.find("div", class_="option-selector option-selector--swatch")
        sabores=[]
        if (sabores_aux != None):
            for s in sabores_aux.find_all("li"):
                sabores.append(s.text.strip())
        else:
            sabores.append("Sin sabor")
        
        url_producto = str(url_raw)+str(url)

        get_imagen_raw(url_raw+str(url), driver)

        reviews_list = get_reviews_raw(url_producto, driver)
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        #almacenamos en la BD
        
        lista_ingredientes = []
        lista_sabores = []
        
        for i in ingredientes:
            i = i.strip()
            ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente = i)[0]
            lista_ingredientes.append(ingrediente_obj)
        for s in sabores:
            s = s.strip()
            sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
            lista_sabores.append(sabor_obj)
        try:
            existe_registro = Producto.objects.filter(url=url_producto).exists()
            if not existe_registro:
                p = Producto.objects.create(nombre = nombre,
                                            marca = brand,                                           
                                            precio = precio,
                                        categoria = categoria,
                                        subcategoria = subcategoria,
                                        stock = stock,
                                        url = url_producto,
                                        rating_original = rating,
                                        )
                producto_id = p.id
                writer.add_document(id_producto = str(producto_id),nombre=nombre, descripcion=descripcion_final, reviews = reviews)
                
                with open('temp.jpg', 'rb') as imagen_file:
                            p.imagen.save("images/"+nombre.strip()+'.jpg', File(imagen_file), save=True)
                os.remove('temp.jpg')
                
                p.sabor.set(lista_sabores)
                p.ingrediente.set(lista_ingredientes)
                print(f"Registro introducido en la BD: {nombre}")
            else:
                print(f"Registro duplicado: {nombre}")
        except IntegrityError as e:
            print(f"Se ha producido un error: {e}")
            print(f"Error al guardar el registro: {nombre}")
        time.sleep(1)
    writer.commit()
    print("Se han cargado " +str(ix.searcher().doc_count()) + "descripciones y reviews")
    return Producto.objects.count()
        
        
def raw_scrap_fat_burners(driver):
    url_fat = str(url_raw)+"/collections/fat-burners"
    f = urllib.request.urlopen(url_fat)
    s = BeautifulSoup(f, "lxml")
    fatList = s.find("div", class_="filters-adjacent collection-listing").find_all("div", class_="block-inner-inner")
    subcategoria_scrapeada = s.find("h1", class_="overlay-text__title super-large-text").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    writer = ix.writer()
    for f in fatList:
        url = f.find("a")['href']
        f = urllib.request.urlopen(url_raw+str(url))
        s = BeautifulSoup(f, "lxml")
        nombre = s.find("div", class_="title-row").text
        marca = "RAW Nutrition"
        brand = Marca.objects.get_or_create(nombre = marca)[0]
        precio = s.find("div", class_="price-area").find("span").text.replace("$", "")
        rating = s.find("div", class_="loox-rating")['data-rating']
        
        descripcion = s.find("div", class_="product-description rte cf").find_all("p")
        descripcion_final = "".join(str(e.text) for e in descripcion)
        stock = True
        stock_div = s.find("div", class_="quantity-submit-row__submit input-row")
    
        if(stock_div == None):
            if(s.find("div", class_="lightly-spaced-row not-in-quickbuy")):
                stock = True
                nombre = nombre + " [EN STOCK A TRAVÉS DE OTRO VENDEDOR]"
            else:
                stock = False
        elif(stock_div.find("div", class_="product-unavailable")):
            stock = False
        else:
            stock = True

        ingredientes_aux = s.find("div", class_="collapsible-tabs").find_all("div", class_="collapsible-tabs__block")
        ingredientes = []
        for i in ingredientes_aux:
            ingredientes.append(i.find("summary").text)
        sabores_aux = s.find("div", class_="option-selector option-selector--swatch")
        sabores=[]
        if (sabores_aux != None):
            for s in sabores_aux.find_all("li"):
                sabores.append(s.text.strip())
        else:
            sabores.append("Sin sabor")

        url_producto = str(url_raw)+str(url)

        get_imagen_raw(url_raw+str(url), driver)

        reviews_list = get_reviews_raw(url_producto, driver)
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        #almacenamos en la BD
        
        lista_ingredientes = []
        lista_sabores = []
        
        for i in ingredientes:
            i = i.strip()
            ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente = i)[0]
            lista_ingredientes.append(ingrediente_obj)
        for s in sabores:
            s = s.strip()
            sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
            lista_sabores.append(sabor_obj)
        try:
            existe_registro = Producto.objects.filter(url=url_producto).exists()
            if not existe_registro:
                p = Producto.objects.create(nombre = nombre,
                                            marca=brand,
                                            precio = precio,
                                        categoria = categoria,
                                        subcategoria = subcategoria,
                                        stock = stock,
                                        url = url_producto,
                                        rating_original = rating,
                                        )
                producto_id = p.id
                writer.add_document(id_producto = str(producto_id),nombre=nombre, descripcion=descripcion_final, reviews = reviews)
                
                with open('temp.jpg', 'rb') as imagen_file:
                            p.imagen.save("images/"+nombre.strip()+'.jpg', File(imagen_file), save=True)
                os.remove('temp.jpg')
                
                p.sabor.set(lista_sabores)
                p.ingrediente.set(lista_ingredientes)
                print(f"Registro introducido en la BD: {nombre}")
            else:
                print(f"Registro duplicado: {nombre}")
        except IntegrityError as e:
            print(f"Se ha producido un error: {e}")
            print(f"Error al guardar el registro: {nombre}")
        time.sleep(1)
    writer.commit()
    print("Se han cargado " +str(ix.searcher().doc_count()) + "descripciones y reviews")
    return Producto.objects.count()
        

def raw_scrap_test_boosters(driver):
    url_test = str(url_raw)+"/collections/test-boosters"
    f = urllib.request.urlopen(url_test)
    s = BeautifulSoup(f, "lxml")
    intraList = s.find("div", class_="filters-adjacent collection-listing").find_all("div", class_="block-inner-inner")
    subcategoria_scrapeada = s.find("h1", class_="overlay-text__title super-large-text").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    writer = ix.writer()
    for i in intraList:
        url = i.find("a")['href']
        f = urllib.request.urlopen(url_raw+str(url))
        s = BeautifulSoup(f, "lxml")
        nombre = s.find("div", class_="title-row").text
        marca = "RAW Nutrition"
        brand = Marca.objects.get_or_create(nombre = marca)[0]
        precio = s.find("div", class_="price-area").find("span").text.replace("$", "")
        rating = s.find("div", class_="loox-rating")['data-rating']
        
        descripcion = s.find("div", class_="product-description rte cf").find_all("p")
        descripcion_final = "".join(str(e.text) for e in descripcion)
        stock = True
        stock_div = s.find("div", class_="quantity-submit-row__submit input-row")
    
        if(stock_div == None):
            if(s.find("div", class_="lightly-spaced-row not-in-quickbuy")):
                stock = True
                nombre = nombre + " [EN STOCK A TRAVÉS DE OTRO VENDEDOR]"
            else:
                stock = False
        elif(stock_div.find("div", class_="product-unavailable")):
            stock = False
        else:
            stock = True

        ingredientes_aux = s.find("div", class_="collapsible-tabs").find_all("div", class_="collapsible-tabs__block")
        ingredientes = []
        for i in ingredientes_aux:
            ingredientes.append(i.find("summary").text)
        sabores_aux = s.find("div", class_="option-selector option-selector--swatch")
        sabores=[]
        if (sabores_aux != None):
            for s in sabores_aux.find_all("li"):
                sabores.append(s.text.strip())
        else:
            sabores.append("Sin sabor")

        url_producto = str(url_raw)+str(url)

        get_imagen_raw(url_raw+str(url), driver)

        reviews_list = get_reviews_raw(url_producto, driver)
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        #almacenamos en la BD
        
        lista_ingredientes = []
        lista_sabores = []
        for i in ingredientes:
            i = i.strip()
            ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente = i)[0]
            lista_ingredientes.append(ingrediente_obj)
        for s in sabores:
            s = s.strip()
            sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
            lista_sabores.append(sabor_obj)
        try:
            existe_registro = Producto.objects.filter(url=url_producto).exists()
            if not existe_registro:
                p = Producto.objects.create(nombre = nombre,
                                            marca=brand,
                                            precio = precio,
                                        categoria = categoria,
                                        subcategoria = subcategoria,
                                        stock = stock,
                                        url = url_producto,
                                        rating_original = rating,
                                        )
                producto_id = p.id
                writer.add_document(id_producto = str(producto_id),nombre=nombre, descripcion=descripcion_final, reviews = reviews)
                
                with open('temp.jpg', 'rb') as imagen_file:
                            p.imagen.save("images/"+nombre.strip()+'.jpg', File(imagen_file), save=True)
                os.remove('temp.jpg')
                
                p.sabor.set(lista_sabores)
                p.ingrediente.set(lista_ingredientes)
                print(f"Registro introducido en la BD: {nombre}")
            else:
                print(f"Registro duplicado: {nombre}")
        except IntegrityError as e:
            print(f"Se ha producido un error: {e}")
            print(f"Error al guardar el registro: {nombre}")
        time.sleep(1)
    writer.commit()
    print("Se han cargado " +str(ix.searcher().doc_count()) + "descripciones y reviews")
    return Producto.objects.count()


def raw_scrap():
    driver = getGeckoDriver()
    raw_scrap_pre_workout(driver)
    raw_scrap_protein(driver)
    raw_scrap_recovery(driver)
    raw_scrap_intra(driver)
    raw_scrap_fat_burners(driver)
    raw_scrap_test_boosters(driver)