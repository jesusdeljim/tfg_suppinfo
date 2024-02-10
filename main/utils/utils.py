from .imports import *

def populate_categorias():
    categorias = ["Proteina", "Desarrollo Muscular", "Energía y resistencia", "Quemadores de grasa y definición", "Salud del Atleta"]
    for nombre in categorias:
        Categoria.objects.create(nombre=nombre)
        
def asignar_subcategoria(subcategoria_scrapeada):
    mapeo_equivalecias = {
        "Preentrenamiento y óxido nítrico": ["Pre-Workout", "Pre-entreno", "Preentrenamiento", "óxido nítrico", "Pre-Entrenamiento", "Suplementos Pre-Entreno"],
        "Proteína Whey" : ["Protein", "Proteínas", "Batidos de proteínas en Polvo"],
        "Aislado de Whey y Whey Nativa" : ["Protein, Proteínas"],
        # Agrega más equivalencias según sea necesario
    }

    for categoria, equivalentes in mapeo_equivalecias.items():
        if subcategoria_scrapeada in equivalentes:
            return categoria

    return subcategoria_scrapeada

def get_imagen_hsn(url):
    req = Request(url = url, headers=headers)
    response = urlopen(req)
    imagen_temp = open('temp.jpg', 'wb')
    imagen_temp.write(response.read())
    imagen_temp.close()

def get_sabores_hsn(url, driver):
    driver.get(url)
    sabores = []
    try:
        sabores_aux = driver.find_element(By.CLASS_NAME, "product_view_Sabor")
        for s in sabores_aux.find_elements(By.TAG_NAME, "option"):
            sabores.append(s.text.strip())
    except:
        sabores.append("Sin sabor") 
    time.sleep(2)
    return sabores
    
def parse_ingredientes_hsn(ingredientes):
    # Utilizar una expresión regular para encontrar elementos fuera de paréntesis
    elementos_fuera = re.findall(r'[^,(]+(?:\([^)]*\)[^,(]*)*', ingredientes)
    # Dividir cada elemento encontrado por comas
    resultado = [elemento.strip() for elemento in elementos_fuera if elemento.strip()]

    return resultado

def get_imagen_raw(url, driver):
    driver.get(url)
    url_imagen = driver.find_element(By.XPATH, "//a[@class='show-gallery']").get_attribute('href')
    response = urlopen(url_imagen)
    imagen_temp = open('temp.jpg', 'wb')
    imagen_temp.write(response.read())
    imagen_temp.close()

def get_reviews_raw(url, driver):
    driver.get(url)
    reviews = []
    reviews_url = driver.find_element(By.XPATH, "//iframe[@id='looxReviewsFrame']").get_attribute('src')
    f = urllib.request.urlopen(reviews_url)
    s = BeautifulSoup(f, "lxml")
    review_nodes = s.find_all("div", class_="main-text")
    for r in review_nodes:
        reviews.append(r.text)
    return reviews