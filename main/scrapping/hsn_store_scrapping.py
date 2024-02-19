from ..utils.imports import *
from ..utils.utils import *

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url_hsn= "https://www.hsnstore.com/nutricion-deportiva"


######################### AMINOACIDOS #########################

def hsn_scrap_isolated_aminoacids(driver, writer):
    url_amino = str(url_hsn)+"/aminoacidos/aislados"
    f = urllib.request.urlopen(url_amino)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_amino+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        aminoList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in aminoList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            
            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]
                           
            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()


def hsn_scrap_bcaa_aminoacids(driver, writer):
    url_amino = str(url_hsn)+"/aminoacidos/bcaa-s-ramificados"
    f = urllib.request.urlopen(url_amino)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    aminoList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in aminoList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]
                        
        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_eaa_aminoacids(driver, writer):
    url_amino = str(url_hsn)+"/aminoacidos/esenciales-eaas"
    f = urllib.request.urlopen(url_amino)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    aminoList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in aminoList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]
                        
        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_glutamine_aminoacids(driver, writer):
    url_amino = str(url_hsn)+"/aminoacidos/glutamina"
    f = urllib.request.urlopen(url_amino)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    aminoList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in aminoList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]
                        
        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_hmb_aminoacids(driver, writer):
    url_amino = str(url_hsn) + "/aminoacidos/hmb"
    f = urllib.request.urlopen(url_amino)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre=cat)[0]
    subcategoria = Subcategoria.objects.get_or_create(nombre=subcat, categoria=categoria)[0]
    aminoList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in aminoList:
        # HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€", "").replace(",", ".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre=marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if stock_div == None:
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)

        # almacenamos en la BD

        lista_ingredientes = []
        lista_sabores = []

        for i in ingredientes:
            i = i.strip()
            ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente=i)[0]
            lista_ingredientes.append(ingrediente_obj)
        for s in sabores:
            s = s.strip()
            sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
            lista_sabores.append(sabor_obj)
        try:
            existe_registro = Producto.objects.filter(url=url_producto).exists()
            if not existe_registro:
                p = Producto.objects.create(nombre=nombre,
                                            marca=brand,
                                            precio=precio,
                                            categoria=categoria,
                                            subcategoria=subcategoria,
                                            stock=stock,
                                            url=url_producto,
                                            rating_original = rating,
                                            )
                producto_id = p.id
                writer.add_document(id_producto = str(producto_id),nombre=nombre, descripcion=descripcion_final, reviews = reviews)

                with open('temp.jpg', 'rb') as imagen_file:
                    p.imagen.save("images/" + nombre.strip() + '.jpg', File(imagen_file), save=True)
                os.remove('temp.jpg')

                p.sabor.set(lista_sabores)
                p.ingrediente.set(lista_ingredientes)
                print(f"Registro introducido en la BD: {nombre}")
            else:
                print(f"Registro duplicado: {nombre}")
        except IntegrityError as e:
            print(f"Se ha producido un error: {e}")
            print(f"Error al guardar el registro: {nombre}")
        time.sleep(10)
    return Producto.objects.count()

###################### NATURAL ANABOLICS ########################

def hsn_scrap_natural_anabolics_cortisol(driver, writer):
    url_nat_anabolics = str(url_hsn)+"/anabolicos-naturales/suplementos-control-cortisol"
    f = urllib.request.urlopen(url_nat_anabolics)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    natAnabolicsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in natAnabolicsList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_natural_anabolics_estrogenos(driver, writer):
    url_nat_anabolics = str(url_hsn)+"/anabolicos-naturales/suplementos-para-control-y-reduccion-estrogenos"
    f = urllib.request.urlopen(url_nat_anabolics)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    natAnabolicsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in natAnabolicsList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_natural_anabolics_pro_hormona_crecimiento(driver, writer):
    url_nat_anabolics = str(url_hsn)+"/anabolicos-naturales/pro-hormona-del-crecimiento"
    f = urllib.request.urlopen(url_nat_anabolics)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    natAnabolicsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in natAnabolicsList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_natural_anabolics_testosterone(driver, writer):
    url_nat_anabolics = str(url_hsn)+"/anabolicos-naturales/pro-testosterona"
    f = urllib.request.urlopen(url_nat_anabolics)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_nat_anabolics+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        carbsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in carbsList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_natural_anabolics_zma(driver, writer):
    url_nat_anabolics = str(url_hsn)+"/anabolicos-naturales/zma"
    f = urllib.request.urlopen(url_nat_anabolics)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    natAnabolicsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in natAnabolicsList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()
################################ BARRITAS ##############################
def hsn_scrap_protein_bars(driver, writer):
    url_bars = str(url_hsn)+"/barritas/proteinas"
    f = urllib.request.urlopen(url_bars)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    barsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in barsList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_energetic_bars(driver, writer):
    url_bars = str(url_hsn)+"/barritas/energeticas"
    f = urllib.request.urlopen(url_bars)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    barsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in barsList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_bars_meal_sustitutive(driver, writer):
    url_bars = str(url_hsn)+"/barritas/sustitutas-de-comida"
    f = urllib.request.urlopen(url_bars)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    barsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in barsList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

################################ CARBOHIDRATOS #########################

def hsn_scrap_carbs(driver, writer):
    url_carbs = str(url_hsn)+"/carbohidratos"
    f = urllib.request.urlopen(url_carbs)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_carbs+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        carbsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in carbsList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()

############################# CONTROL DE PESO ##############################

def hsn_scrap_weight_control_fat_block(driver, writer):
    url_weight_control = str(url_hsn)+"/controlar-peso/bloqueadores-grasas-carbohidratos"
    f = urllib.request.urlopen(url_weight_control)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    weightControlList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in weightControlList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_weight_control_hunger_control(driver, writer):
    url_weight_control = str(url_hsn)+"/controlar-peso/inhibidores-apetito"
    f = urllib.request.urlopen(url_weight_control)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_weight_control+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        weightControlList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in weightControlList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_weight_control_reduction(driver, writer):
    url_weight_control = str(url_hsn)+"/controlar-peso/cremas-reductoras"
    f = urllib.request.urlopen(url_weight_control)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    weightControlList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in weightControlList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_weight_control_diuretics(driver, writer):
    url_weight_control = str(url_hsn)+"/controlar-peso/diureticos"
    f = urllib.request.urlopen(url_weight_control)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_weight_control+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        weightControlList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in weightControlList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_weight_control_termogenics(driver, writer):
    url_weight_control = str(url_hsn)+"/controlar-peso/termogenicos"
    f = urllib.request.urlopen(url_weight_control)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_weight_control+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        weightControlList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in weightControlList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_weight_control_termo_no_stim(driver, writer):
    url_weight_control = str(url_hsn)+"/controlar-peso/quemadores-termogenicos-sin-estimulantes"
    f = urllib.request.urlopen(url_weight_control)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_weight_control+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        weightControlList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in weightControlList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()


############################ CREATINE ###########################
def hsn_scrap_creatine(driver, writer):
    url_creatine = str(url_hsn)+"/creatina"
    f = urllib.request.urlopen(url_creatine)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    creatineList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in creatineList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()
############################### GANADORES DE PESO #########################
def hsn_scrap_mass_gainer(driver, writer):
    url_mass_gainer = str(url_hsn)+"/ganadores-de-peso"
    f = urllib.request.urlopen(url_mass_gainer)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    gainerList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in gainerList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count() 

############################### INTRA ENTRENAMIENTO #######################

def hsn_scrap_intra(driver, writer):
    url_intra = str(url_hsn)+"/intra-entrenamiento"
    f = urllib.request.urlopen(url_intra)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    intraList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in intraList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

############################### MINERALES ##########################

def hsn_scrap_minerals(driver, writer):
    url_minerals = str(url_hsn)+"/minerales"
    f = urllib.request.urlopen(url_minerals)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_minerals+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        mineralsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in mineralsList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()  

def hsn_scrap_multivitamins(driver, writer):
    url_multivitamins = str(url_hsn)+"/multivitaminicos"
    f = urllib.request.urlopen(url_multivitamins)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_multivitamins+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        multiVitaminsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in multiVitaminsList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()    

def hsn_scrap_recovery(driver, writer):
    url_recovery = str(url_hsn)+"/post-entrenamiento-y-recuperacion"
    f = urllib.request.urlopen(url_recovery)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_recovery+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        recoveryList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in recoveryList:
            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count()   

def hsn_scrap_pre_workout(driver, writer):
    url_pre_workout = str(url_hsn)+"/pre-entrenamiento"
    f = urllib.request.urlopen(url_pre_workout)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_pre_workout+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        preWorkoutList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in preWorkoutList:
            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
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
            time.sleep(10)
    return Producto.objects.count() 

######################### PROTEINAS ######################
def hsn_scrap_protein_casein(driver, writer):
    url_protein = str(url_hsn)+"/proteinas/caseina"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in proteinList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_protein_huevo(driver, writer):
    url_protein = str(url_hsn)+"/proteinas/albumina-de-huevo"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in proteinList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_protein_carne(driver, writer):
    url_protein = str(url_hsn)+"/proteinas/carne"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in proteinList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_protein_secuencial(driver, writer):
    url_protein = str(url_hsn)+"/proteinas/liberacion-secuencial"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in proteinList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_protein_vegetal(driver, writer):
    url_protein = str(url_hsn)+"/proteinas/vegetales"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in proteinList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_protein_whey_iso(driver, writer):
    url_protein = str(url_hsn)+"/proteinas/whey/aislados-de-suero"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in proteinList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_protein_whey_concentrated(driver, writer):
    url_protein = str(url_hsn)+"/proteinas/whey/concentrados-de-suero"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in proteinList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()

def hsn_scrap_protein_whey_hydro(driver, writer):
    url_protein = str(url_hsn)+"/proteinas/whey/hidrolizadas"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
    proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
    for a in proteinList:

        #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
        url_imagen = a.find("img", class_="lazyload")['data-src']
        get_imagen_hsn(url_imagen)
        url_producto = a.find("a", class_="product-image")['href']
        f = urllib.request.urlopen(url_producto)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", itemprop="name").text
        precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
        marca = "HSN"
        brand = Marca.objects.get_or_create(nombre = marca)[0]

        rating = 0.0
        try:
            rating_divs = s.find("div", class_="ratings").find_all("i")
            for r in rating_divs:
                if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                    rating += 1.0
                elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                    rating += 0.5
                else:
                    rating += 0.0
        except:
            rating = 0.0
        
        descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

        reviews_list = []
        try:
            reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
            for r in reviews_divs:
                reviews_list.append(r.find("p", class_="content-review").text)
        except:
            reviews_list.append("No hay reviews")
        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        stock = True
        stock_div = s.find("div", class_="no-stock-block")
        if(stock_div == None):
            stock = True
        else:
            stock = False

        try:
            ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
            ingredientes = parse_ingredientes(ingredientes_aux)
        except:
            ingredientes_aux = s.find("div", class_="table_ingredientes")
            try:
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes = [nombre.split(" ")[0]]

        sabores = get_sabores_hsn(url_producto, driver)
        
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
        time.sleep(10)
    return Producto.objects.count()


def hsn_scrap_vitamins(driver, writer):
    url_vitamins = str(url_hsn)+"/vitaminas"
    f = urllib.request.urlopen(url_vitamins)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
    subcat = asignar_subcategoria(subcategoria_scrapeada)
    cat = asignar_categoria(subcat)
    categoria = Categoria.objects.get_or_create(nombre=cat)[0] 
    subcategoria = Subcategoria.objects.get_or_create(nombre=subcat, categoria=categoria)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_vitamins+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        vitaminsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in vitaminsList:
            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("img", class_="lazyload")['data-src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre=marca)[0]

            rating = 0.0
            try:
                rating_divs = s.find("div", class_="ratings").find_all("i")
                for r in rating_divs:
                    if(r['class'][0] == "fas" and r['class'][1]== "fa-star"):
                        rating += 1.0
                    elif(r['class'][0] == "fa" and r['class'][1] == "fa-star-half-alt"):
                        rating += 0.5
                    else:
                        rating += 0.0
            except:
                rating = 0.0
            
            descripcion_final = s.find("div", class_="col-xs-12 no-padding-lat product_desc").find("p").text

            reviews_list = []
            try:
                reviews_divs = s.find("ul", class_="col-xs-12 reviews-comment-box").find_all("li")
                for r in reviews_divs:
                    reviews_list.append(r.find("p", class_="content-review").text)
            except:
                reviews_list.append("No hay reviews")
            reviews = "|writer_split|".join(str(e) for e in reviews_list)
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes(ingredientes_aux)
                except:
                    ingredientes = [nombre.split(" ")[0]]

            sabores = get_sabores_hsn(url_producto, driver)
            
            #almacenamos en la BD
        
            lista_ingredientes = []
            lista_sabores = []
            
            for i in ingredientes:
                i = i.strip()
                ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente=i)[0]
                lista_ingredientes.append(ingrediente_obj)
            for s in sabores:
                s = s.strip()
                sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
                lista_sabores.append(sabor_obj)
            try:
                existe_registro = Producto.objects.filter(url=url_producto).exists()
                if not existe_registro:
                    p = Producto.objects.create(nombre=nombre,
                                                marca=brand,
                                                precio=precio,
                                                categoria=categoria,
                                                subcategoria=subcategoria,
                                                stock=stock,
                                                url=url_producto,
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
            time.sleep(10)
    return Producto.objects.count() 




def hsn_scrap(driver, writer):
    print("HSN Scrapping started")
    hsn_scrap_isolated_aminoacids(driver, writer)
    hsn_scrap_bcaa_aminoacids(driver, writer)
    hsn_scrap_eaa_aminoacids(driver, writer)
    hsn_scrap_glutamine_aminoacids(driver, writer)
    hsn_scrap_hmb_aminoacids(driver, writer)
    hsn_scrap_natural_anabolics_cortisol(driver, writer)
    hsn_scrap_natural_anabolics_estrogenos(driver, writer)
    hsn_scrap_natural_anabolics_pro_hormona_crecimiento(driver, writer)
    hsn_scrap_natural_anabolics_testosterone(driver, writer)
    hsn_scrap_natural_anabolics_zma(driver, writer)
    hsn_scrap_protein_bars(driver, writer)
    hsn_scrap_energetic_bars(driver, writer)
    hsn_scrap_bars_meal_sustitutive(driver, writer)
    hsn_scrap_carbs(driver, writer)
    hsn_scrap_weight_control_fat_block(driver, writer)
    hsn_scrap_weight_control_hunger_control(driver, writer)
    hsn_scrap_weight_control_reduction(driver, writer)
    hsn_scrap_weight_control_diuretics(driver, writer)
    hsn_scrap_weight_control_termogenics(driver, writer)
    hsn_scrap_weight_control_termo_no_stim(driver, writer)
    hsn_scrap_creatine(driver, writer)
    hsn_scrap_mass_gainer(driver, writer)
    hsn_scrap_intra(driver, writer)
    hsn_scrap_minerals(driver, writer)
    hsn_scrap_multivitamins(driver, writer)
    hsn_scrap_recovery(driver, writer)
    hsn_scrap_pre_workout(driver, writer)
    hsn_scrap_protein_casein(driver, writer)
    hsn_scrap_protein_huevo(driver, writer)
    hsn_scrap_protein_carne(driver, writer)
    hsn_scrap_protein_secuencial(driver, writer)
    hsn_scrap_protein_vegetal(driver, writer)
    hsn_scrap_protein_whey_iso(driver, writer)
    hsn_scrap_protein_whey_concentrated(driver, writer)
    hsn_scrap_protein_whey_hydro(driver, writer)
    hsn_scrap_vitamins(driver, writer)
    print("HSN Scrapping finished successfully")
