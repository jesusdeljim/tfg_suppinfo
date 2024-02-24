from main.utils.imports import *
from main.utils.utils import *

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url_hsn= "https://www.hsnstore.com/nutricion-deportiva"

urls_hsn = ["/aminoacidos/aislados", "/aminoacidos/bcaa-s-ramificados", "/aminoacidos/esenciales-eaas", "/aminoacidos/glutamina", "/aminoacidos/hmb", "/anabolicos-naturales/suplementos-control-cortisol", "/anabolicos-naturales/suplementos-para-control-y-reduccion-estrogenos", "/anabolicos-naturales/pro-hormona-del-crecimiento", "/anabolicos-naturales/pro-testosterona", "/anabolicos-naturales/zma", "/barritas/proteinas", "/barritas/energeticas", "/barritas/sustitutas-de-comida", "/carbohidratos","/controlar-peso/bloqueadores-grasas-carbohidratos", "/controlar-peso/inhibidores-apetito","/controlar-peso/cremas-reductoras","/controlar-peso/diureticos","/controlar-peso/termogenicos","/controlar-peso/quemadores-termogenicos-sin-estimulantes","/creatina","/ganadores-de-peso","/intra-entrenamiento","/minerales","/multivitaminicos","/post-entrenamiento-y-recuperacion","/pre-entrenamiento", "/proteinas/caseina", "/proteinas/albumina-de-huevo", "/proteinas/carne", "/proteinas/liberacion-secuencial", "/proteinas/vegetales", "/proteinas/whey/aislados-de-suero", "/proteinas/whey/concentrados-de-suero", "/proteinas/whey/hidrolizadas", "/vitaminas"]

def hsn_scrap_complete(driver, writer):
    for u in urls_hsn:
        url_categoria = str(url_hsn)+str(u)
        f = urllib.request.urlopen(url_categoria)
        s = BeautifulSoup(f, "lxml")
        try:
            num_pags = int(s.find("div", class_="pages").find_all("li")[-2].text)
        except:
            num_pags = 1
        subcategoria_scrapeada = s.find("div", class_="page-title category-title").find("span").text.strip()
        subcat = asignar_subcategoria(subcategoria_scrapeada)
        cat = asignar_categoria(subcat)
        categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
        subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
        if int(num_pags) > 1:
            for pag in range(1,num_pags+1):
                f = urllib.request.urlopen(url_categoria+"?p="+str(pag))
                s = BeautifulSoup(f, "lxml")
                time.sleep(3)
                try:
                    pList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
                except:
                    pList = []
                if len(pList) == 0:
                    continue
                for a in pList:
                    try:
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
                    except Exception as e:
                        print(f"Se ha producido un error al scrapear el producto: {nombre}")
                        print(f"Error: {e}")
                        continue
        else:
            try:
                pList = s.find("ul", class_="products-grid").find_all("li", class_="item last")
            except:
                pList = []
            if len(pList) == 0:
                continue
            for a in pList:
                    try:
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
                    except Exception as e:
                        print(f"Se ha producido un error al scrapear el producto: {nombre}")
                        print(f"Error: {e}")
                        continue
    return Producto.objects.count()

def hsn_scrap(driver, writer):
    print("HSN Scrapping started")
    hsn_scrap_complete(driver, writer)
    print("HSN Scrapping finished successfully")
