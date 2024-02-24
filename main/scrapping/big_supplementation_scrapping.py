from main.utils.imports import *
from main.utils.utils import *


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url_big = "https://bigsupps.site"
urls_big = ["https://bigsupps.site/collections/aminoacids", "https://bigsupps.site/collections/testosterone", "https://bigsupps.site/collections/protein", "https://bigsupps.site/collections/pre-workout", "https://bigsupps.site/collections/fat-burner", "https://bigsupps.site/collections/mass-gainer", "https://bigsupps.site/collections/micronutrients", "https://bigsupps.site/collections/snacks"]

def big_scrap_complete(driver, writer):
    for url in urls_big:
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f, "lxml")
        time.sleep(2)
        try:
            num_pags = s.find("div", class_="pagination has-margin-top-6 has-margin-bottom-6").find_all("span")[-2].text
        except:
            num_pags = 1
        subcategoria_scrapeada = s.find("h2", class_="has-text-weight-bold is-uppercase is-size-2-widescreen is-size-3-tablet is-size-5-mobile has-padding-bottom-3").text.strip()
        subcat = asignar_subcategoria(subcategoria_scrapeada)
        cat = asignar_categoria(subcat)
        categoria = Categoria.objects.get_or_create(nombre=cat)[0]
        subcategoria = Subcategoria.objects.get_or_create(nombre=subcat, categoria=categoria)[0]
        if int(num_pags) > 1:
            for pag in range(1, int(num_pags) + 1):
                f = urllib.request.urlopen(str(url) + "?page=" + str(pag))
                s = BeautifulSoup(f, "lxml")
                time.sleep(2)
                pList = s.find("div", class_="product-list").find_all("div", class_="product-block detail-mode-permanent fixed-width")
                for p in pList:
                    try:
                        url_p = p.find("a", class_="product-link")['href']
                        f = urllib.request.urlopen(str(url_big) + str(url_p))
                        s = BeautifulSoup(f, "lxml")
                        url_producto = str(url_big) + str(url_p)
                        nombre = s.find("h1", class_="title").text.strip()
                        precio = s.find("div", class_="price-text after").find("span").text.replace("€", "").replace(",", ".").strip()
                        marca = "BIG SUPPS"
                        brand = Marca.objects.get_or_create(nombre=marca)[0]
                        rating = get_rating_big(url_producto, driver)
                        stock = True
                        try:
                            stock_label = s.find("div", class_="column detail").find("span", class_="productlabel soldout").text
                            stock = False
                        except:
                            stock = True
                        url_imagen = "https:" + s.find("div", class_="main-image").find("noscript").find("img")['src']
                        get_imagen_big(url_imagen)

                        sabores = get_sabores_big(url_producto, driver)
                        descripcion_final = get_descripcion_big(s)
                        ingredientes = get_ingredientes_big(url_producto, driver)
                        reviews_list = get_reviews_big(url_producto, driver)
                        reviews = "|writer_split|".join(str(e) for e in reviews_list)

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
                                                            rating_original=rating,
                                                            )
                                producto_id = p.id
                                writer.add_document(id_producto=str(producto_id), nombre=nombre, descripcion=descripcion_final, reviews=reviews)

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
                        time.sleep(8)
                    except Exception as e:
                        print(f"Se ha producido un error: {e}")
                        continue
        else:
            pList = s.find("div", class_="product-list").find_all("div", class_="product-block detail-mode-permanent fixed-width")
            for p in pList:
                    try:
                        url = p.find("a", class_="product-link")['href']
                        f = urllib.request.urlopen(str(url_big) + str(url))
                        s = BeautifulSoup(f, "lxml")

                        url_producto = str(url_big) + str(url)
                        nombre = s.find("h1", class_="title").text.strip()
                        precio = s.find("div", class_="price-text after").find("span").text.replace("€", "").replace(",", ".").strip()
                        marca = "BIG SUPPS"
                        brand = Marca.objects.get_or_create(nombre=marca)[0]
                        rating = get_rating_big(url_producto, driver)
                        stock = True
                        try:
                            stock_label = s.find("div", class_="column detail").find("span", class_="productlabel soldout").text
                            stock = False
                        except:
                            stock = True
                        url_imagen = "https:" + s.find("div", class_="main-image").find("noscript").find("img")['src']
                        get_imagen_big(url_imagen)

                        sabores = get_sabores_big(url_producto, driver)
                        descripcion_final = get_descripcion_big(s)
                        ingredientes = get_ingredientes_big(url_producto, driver)
                        reviews_list = get_reviews_big(url_producto, driver)
                        reviews = "|writer_split|".join(str(e) for e in reviews_list)

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
                                                            rating_original=rating,
                                                            )
                                producto_id = p.id
                                writer.add_document(id_producto=str(producto_id), nombre=nombre, descripcion=descripcion_final, reviews=reviews)

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
                        time.sleep(8)
                    except Exception as e:
                        print(f"Se ha producido un error: {e}")
                        continue
    return Producto.objects.count()
            
def big_scrap(driver, writer):
    print("Big Supplementation scraping started")
    big_scrap_complete(driver, writer)
    print("Big Supplementation scraping finished successfully")
    