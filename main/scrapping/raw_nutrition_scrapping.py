from main.utils.imports import *
from main.utils.utils import *

if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
    ssl, "_create_unverified_context", None
):
    ssl._create_default_https_context = ssl._create_unverified_context

url_raw = "https://getrawnutrition.com"
urls_raw = [
    "https://getrawnutrition.com/collections/pre-workout",
    "https://getrawnutrition.com/collections/protein",
    "https://getrawnutrition.com/collections/recovery",
    "https://getrawnutrition.com/collections/pump",
    "https://getrawnutrition.com/collections/fat-burners",
    "https://getrawnutrition.com/collections/test-boosters",
]


def raw_scrap_complete(driver, writer):
    for url in urls_raw:
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f, "lxml")
        pList = s.find("div", class_="filters-adjacent collection-listing").find_all(
            "div", class_="block-inner-inner"
        )
        subcategoria_scrapeada = s.find(
            "h1", class_="overlay-text__title super-large-text"
        ).text.strip()
        subcat = asignar_subcategoria(subcategoria_scrapeada)
        cat = asignar_categoria(subcat)
        categoria = Categoria.objects.get_or_create(nombre=cat)[0]
        subcategoria = Subcategoria.objects.get_or_create(
            nombre=subcat, categoria=categoria
        )[0]
        for e in pList:
            try:
                url = e.find("a")["href"]
                f = urllib.request.urlopen(url_raw + str(url))
                s = BeautifulSoup(f, "lxml")

                nombre = s.find("div", class_="title-row").text

                marca = "RAW Nutrition"
                brand = Marca.objects.get_or_create(nombre=marca)[0]

                precio = (
                    s.find("div", class_="price-area")
                    .find("span")
                    .text.replace("$", "")
                )

                rating = s.find("div", class_="loox-rating")["data-rating"]

                descripcion = s.find(
                    "div", class_="product-description rte cf"
                ).find_all("p")
                descripcion_final = "".join(str(e.text) for e in descripcion)

                stock = True
                stock_div = s.find(
                    "div", class_="quantity-submit-row__submit input-row"
                )

                if stock_div == None:
                    if s.find("div", class_="lightly-spaced-row not-in-quickbuy"):
                        stock = True
                        nombre = nombre + " [EN STOCK A TRAVÉS DE OTRO VENDEDOR]"
                    else:
                        stock = False
                elif stock_div.find("div", class_="product-unavailable"):
                    stock = False
                else:
                    stock = True

                ingredientes_aux = s.find("div", class_="collapsible-tabs").find_all(
                    "div", class_="collapsible-tabs__block"
                )
                ingredientes = []
                for i in ingredientes_aux:
                    ingredientes.append(i.find("summary").text)

                sabores_aux = s.find(
                    "div", class_="option-selector option-selector--swatch"
                )
                sabores = []
                if sabores_aux != None:
                    for s in sabores_aux.find_all("li"):
                        sabores.append(s.text.strip())
                else:
                    sabores.append("Sin sabor")

                url_producto = str(url_raw) + str(url)

                get_imagen_raw(url_raw + str(url), driver)

                reviews_list = get_reviews_raw(url_producto, driver)
                reviews = "|writer_split|".join(str(e) for e in reviews_list)
                # almacenamos en la BD

                lista_ingredientes = []
                lista_sabores = []

                for i in ingredientes:
                    i = i.strip()
                    ingrediente_obj = Ingrediente.objects.get_or_create(ingrediente=i)[
                        0
                    ]
                    lista_ingredientes.append(ingrediente_obj)
                for s in sabores:
                    s = s.strip()
                    sabor_obj = Sabor.objects.get_or_create(sabor=s)[0]
                    lista_sabores.append(sabor_obj)

                try:
                    existe_registro = Producto.objects.filter(url=url_producto).exists()
                    if not existe_registro:
                        p = Producto.objects.create(
                            nombre=nombre,
                            marca=brand,
                            precio=precio,
                            categoria=categoria,
                            subcategoria=subcategoria,
                            stock=stock,
                            url=url_producto,
                            rating_original=rating,
                        )
                        producto_id = p.id
                        writer.add_document(
                            id_producto=str(producto_id),
                            nombre=nombre,
                            descripcion=descripcion_final,
                            reviews=reviews,
                        )
                        with open("temp.jpg", "rb") as imagen_file:
                            p.imagen.save(
                                "images/" + nombre.strip() + ".jpg",
                                File(imagen_file),
                                save=True,
                            )
                        os.remove("temp.jpg")

                        p.sabor.set(lista_sabores)
                        p.ingrediente.set(lista_ingredientes)
                        print(f"Registro introducido en la BD: {nombre}")
                    else:
                        print(f"Registro duplicado: {nombre}")
                except IntegrityError as e:
                    print(f"Se ha producido un error: {e}")
                    print(f"Error al guardar el registro: {nombre}")
                    continue
                time.sleep(1)
            except Exception as e:
                print(f"Se ha producido un error al scrapear el producto: {nombre}")
                print(f"Error: {e}")
                continue
    return Producto.objects.count()


def raw_scrap(driver, writer):
    print("RAW Nutrition scraping started")
    raw_scrap_complete(driver, writer)
    print("RAW Nutrition scraping finished successfully")
