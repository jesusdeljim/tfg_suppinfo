from main.utils.imports import *
from main.utils.utils import *

prozis_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'cookie': '__vh_ot=5511135396.1684061396; CookieConsent={stamp:%27MCixUvelPGy6k46gk5VnPKEj/KM/iRqm3Yb424a3dBCmTOZOiH9VPw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:2%2Cutc:1685391969105%2Cregion:%27es%27}; _stlg=es%2Fes; __cph_ot=5511135396.1708194372.Direto; _am=web; __aid_ot=bc5628cf.1708194372; przsid=rrbmnlf8lr3e7h4rbvth6130pv; __cfruid=c5d119480b21769b1df973c9bcb787bde2da76eb-1708194372; __mub=v2:{"rid":"s90jpv-3bo-52-2521","or":"920bcc41","rf":"8df75fb6"}; __sid_ot=2339244198.1708194372; __cf_bm=QjH4_FSig_eyhrb.3YKHQ5eixDlBDeWTaOxUGuIzV1A-1708196169-1.0-AT/rCOoiAvYwwp4ocQIBno8YmrT06yJCPKbjmpUZ9ougNfyRGjlu2V+d7gT4ZyjoBnhKyfIV1tIMWN4jLGxBm3AcC4rCLFlkdVTHaOr3Gwvb; __rridul=s90jpv-3bo-52-2521'
}
url_prozis = "https://www.prozis.com/es/es/nutricion-deportiva"

req = Request(url_prozis, headers=prozis_headers)

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def prozis_scrap_complete(driver,writer):
    driver.get(url_prozis)   
    time.sleep(2)
    driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click() 
    num_pags = driver.find_elements(By.CLASS_NAME, "pagination-button")[-2].text
    urls_productos = []
    for pag in range(1,int(num_pags)+1): 
        driver.get(url_prozis + f"/q/page/{pag}")
        time.sleep(4)
        productos = driver.find_element(By.CLASS_NAME, "row.list-container").find_elements(By.CLASS_NAME, "col.list-item")
        for producto in productos:
            url_producto = producto.find_element(By.TAG_NAME, "a").get_attribute("href")
            urls_productos.append(url_producto)
    for url_producto in urls_productos:
        try:
            driver.get(url_producto)
            time.sleep(4)
            try:
                driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click() 
            except:
                pass
            subcategoria_scrapeada = driver.find_element(By.ID, "breadcrumbs").find_elements(By.TAG_NAME, "a")[-2].text.strip()
            subcat = asignar_subcategoria(subcategoria_scrapeada)
            if subcat == "No subcategoria asignada":
                continue
            cat = asignar_categoria(subcat)
            categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
            subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
            nombre = driver.find_element(By.ID, "breadcrumbs").find_elements(By.TAG_NAME, "a")[-1].text.strip()
            print("Intentando scraping producto: ", nombre)
            precio = driver.find_element(By.XPATH, "//p[@class='final-price']").get_attribute("data-qa").replace("€", "").replace(",",".").strip()
            marca = "PROZIS"
            brand = Marca.objects.get_or_create(nombre = marca)[0]
            rating = driver.find_element(By.CLASS_NAME, "prz-blk-content-rating").find_element(By.TAG_NAME, "span").text.split("/")[0].strip()
            stock = True
            stock_div = driver.find_element(By.CLASS_NAME, "stock-info").text.strip()
            if "No disponible" in stock_div:
                stock = False
            else:
                stock = True
            
            url_imagen = driver.find_element(By.CLASS_NAME, "first-column").find_element(By.TAG_NAME, "img").get_attribute("src")
            get_imagen_prozis(url_imagen)

            sabores = []
            ingredientes = []
            elements = driver.find_elements(By.CLASS_NAME, "prz-blk-content")
            for element in elements:
                # Verifica si el elemento contiene un <i> con la clase 'prz-fullscreen'
                if not element.find_elements(By.CSS_SELECTOR, "i.prz-fullscreen"):
                    # Si no lo contiene, verifica si tiene un <span> con el texto 'Información Nutricional'
                    if element.find_elements(By.XPATH, ".//span[contains(text(), 'Información Nutricional')]") or element.find_elements(By.XPATH, ".//span[contains(text(), 'Información del producto')]"):
                        element.click()
                        break
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, "nut-tbl-select-box").click()
                for sabor in driver.find_elements(By.TAG_NAME, "li"):
                    sabores.append(sabor.text)
                
            except NoSuchElementException:
                sabores.append("Sabor único")
            sabores = list(filter(None, sabores))
            try:
                ingredientes_text = driver.find_element(By.CLASS_NAME, "nut-other-ingredients").find_element(By.CLASS_NAME, "list").text
                ingredientes_text = ingredientes_text[:-1]
                ingredientes = parse_ingredientes(ingredientes_text)
            except:
                ingredientes.append("Sin ingredientes")
            driver.find_element(By.ID, "contentCloseBtn").click() #Cierra menu info nutricional
            time.sleep(1)

            #Buscamos de nuevo el elemento "prz-blk-content", pero en vez de coger el primero cogemos el siguiente, que sera el de las reviews
            elements = driver.find_elements(By.CLASS_NAME, "prz-blk-content")
            for element in elements:
                # Verifica si el elemento contiene un <i> con la clase 'prz-fullscreen'
                if not element.find_elements(By.CSS_SELECTOR, "i.prz-fullscreen"):
                    # Si no lo contiene, verifica si tiene un <span> con el texto 'Opiniones generales'
                    if element.find_elements(By.XPATH, ".//span[contains(text(), 'Opiniones generales')]"):
                        element.click()
                        break
            time.sleep(2)
            try:
                reviews_divs = driver.find_element(By.CLASS_NAME, "reviews-section.customer-reviews").find_elements(By.CLASS_NAME, "review-detailed")
                reviews_list=[]
                for review in reviews_divs:
                    reviews_list.append(review.find_element(By.CLASS_NAME, "review-content").text)

                reviews = "|writer_split|".join(str(e) for e in reviews_list)
            except:
                reviews = "No hay reviews"
            
            driver.find_element(By.ID, "contentCloseBtn").click() #Cierra menu reviews
            time.sleep(2)
            try:
                driver.find_element(By.CLASS_NAME, "prz-blk-content.pdp-block-horizontal.prz-blk-content-with-img").click() #Abre menu descripciones
                time.sleep(2)
                descripcion = ""
                table_descripciones = driver.find_element(By.CLASS_NAME, "p-0").find_elements(By.TAG_NAME, "p")

                for p in table_descripciones:
                    if p.text.startswith("*"):
                        continue
                    descripcion += p.text + "\n"

                descripcion_final = descripcion
            except:
                descripcion_final = "No hay descripción"

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
        except Exception as e:
            print(f"Se ha producido un error al scrapear el producto: {nombre}")
            print(f"Error: {e}")
            continue
    return Producto.objects.count()

def prozis_scrap(driver, writer):
    print("Prozis Scraping started")
    prozis_scrap_complete(driver, writer)
    print("Prozis Scraping finished")