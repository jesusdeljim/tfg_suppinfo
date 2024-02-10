from ..utils.imports import *
from ..utils.utils import *

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url_hsn= "https://www.hsnstore.com/nutricion-deportiva"



def hsn_scrap_aminoacids(driver):
    url_amino = str(url_hsn)+"/aminoacidos"
    f = urllib.request.urlopen(url_amino)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_amino+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        aminoList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in aminoList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_natural_anabolics(driver):
    url_nat_anabolics = str(url_hsn)+"/anabolicos-naturales"
    f = urllib.request.urlopen(url_nat_anabolics)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_nat_anabolics+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        natAnabolicsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in natAnabolicsList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_carbs(driver):
    url_carbs = str(url_hsn)+"/carbohidratos"
    f = urllib.request.urlopen(url_carbs)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_carbs+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        carbsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in carbsList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_weight_control(driver):
    url_weight_control = str(url_hsn)+"/controlar-peso"
    f = urllib.request.urlopen(url_weight_control)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_weight_control+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        weightControlList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in weightControlList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_minerals(driver):
    url_minerals = str(url_hsn)+"/minerales"
    f = urllib.request.urlopen(url_minerals)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_minerals+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        mineralsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in mineralsList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_multivitamins(driver):
    url_multivitamins = str(url_hsn)+"/multivitaminicos"
    f = urllib.request.urlopen(url_multivitamins)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_multivitamins+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        multiVitaminsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in multiVitaminsList:

            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_recovery(driver):
    url_recovery = str(url_hsn)+"/post-entrenamiento-y-recuperacion"
    f = urllib.request.urlopen(url_recovery)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_recovery+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        recoveryList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in recoveryList:
            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_pre_workout(driver):
    url_pre_workout = str(url_hsn)+"/pre-entrenamiento"
    f = urllib.request.urlopen(url_pre_workout)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_pre_workout+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        preWorkoutList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in preWorkoutList:
            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_protein(driver):
    url_protein = str(url_hsn)+"/proteinas"
    f = urllib.request.urlopen(url_protein)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_protein+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        proteinList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in proteinList:
            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap_vitamins(driver):
    url_vitamins = str(url_hsn)+"/vitaminas"
    f = urllib.request.urlopen(url_vitamins)
    s = BeautifulSoup(f, "lxml")
    num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
    cat = s.find("div", class_="page-title category-title").find("span").text.strip
    categoria = Categoria.objects.get_or_create(nombre = cat)[0]
    for pag in range(1,num_pags+1):
        f = urllib.request.urlopen(url_vitamins+"?p="+str(pag))
        s = BeautifulSoup(f, "lxml")
        time.sleep(3)
        vitaminsList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
        for a in vitaminsList:
            #HAY QUE ARREGLAR LA IMAGEN NO SE CAPTURA BIEN
            url_imagen = a.find("a", class_="product-image").find("img")['src']
            get_imagen_hsn(url_imagen)
            url_producto = a.find("a", class_="product-image")['href']
            f = urllib.request.urlopen(url_producto)
            s = BeautifulSoup(f, "lxml")

            nombre = s.find("h1", itemprop="name").text
            precio = s.find("div", class_="final-price").text.replace("€","").replace(",",".").strip()
            marca = "HSN"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            stock = True
            stock_div = s.find("div", class_="no-stock-block")
            if(stock_div == None):
                stock = True
            else:
                stock = False

            try:
                ingredientes_aux = s.find("div", class_="table_ingredientes").find_all("p")[1].text.split(".")[0]
                ingredientes = parse_ingredientes_hsn(ingredientes_aux)
            except:
                ingredientes_aux = s.find("div", class_="table_ingredientes")
                try:
                    ingredientes = parse_ingredientes_hsn(ingredientes_aux)
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
                                            stock = stock,
                                            url = url_producto,
                                            )
                    #producto_id = p.id
                    
                    with open('temp.jpg', 'rb') as imagen_file:
                                p.imagen.save("images/"+nombre.strip()+'.webp', File(imagen_file), save=True)
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

def hsn_scrap():
    
    driver = getGeckoDriver()
    hsn_scrap_aminoacids(driver)
    hsn_scrap_carbs(driver)
    hsn_scrap_minerals(driver)
    hsn_scrap_multivitamins(driver)
    hsn_scrap_natural_anabolics(driver)
    hsn_scrap_pre_workout(driver)
    hsn_scrap_protein(driver)
    hsn_scrap_weight_control(driver)
    hsn_scrap_recovery(driver)
    hsn_scrap_vitamins(driver)


    