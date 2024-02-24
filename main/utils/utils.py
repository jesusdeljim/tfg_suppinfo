from .imports import *

mapeo_subcategorias = {
        "Preentrenamiento y Óxido Nítrico": ["Pre-Workout", "Pre-entreno", "Preentrenamiento", "Preentrenamiento y Óxido Nítrico", "óxido nítrico", "Pre-Entrenamiento", "Suplementos Pre-Entreno", "Pre-entrenos"],
        "Proteína Whey" : ["Proteína Whey","Protein", "Proteínas", "Batidos de proteínas en Polvo", "Proteínas Aisladas de Suero", "Proteínas Concentradas de Suero", " Proteína Whey "],
        "Aislado de Whey y Whey Nativa" : ["Aislado de Whey y Whey Nativa","Protein", "Proteínas", "Batidos de proteínas en Polvo", "Proteínas Aisladas de Suero", "Proteínas Concentradas de Suero"],
        "Hidrolizado de Proteína Whey" : ["Hidrolizado de Proteína Whey","Proteínas Hidrolizadas"],
        "Caseína e Proteína de liberación lenta" : ["Caseína e Proteína de liberación lenta","Caseínas", "Proteínas Liberación Secuencial"],
        "Proteína de Huevo y de Carne" : ["Proteína de Huevo y de Carne","Proteínas de Albúmina de Huevo", "Proteínas de Carne"],
        "Ganadores de Masa" : ["Ganadores de Masa", "Ganadores de Peso"],
        "Proteína Vegetal" : ["Proteína Vegetal", "Proteínas Vegetales"],
        "Colágeno" : ["Colágeno"],
        "Proteína Dietética" : ["Proteína Dietética"],
        "Barritas Proteicas" : ["Barritas Proteicas", "Barritas de Proteínas", "Snacks Proteicos"],
        "Snacks Proteicos" : ["Snacks Proteicos","Barritas de Proteínas", "Sustitutas de Comida", "Snacks Proteicos"],
        "Alimentación Proteica" : ["Alimentación Proteica","Barritas de Proteínas", "Sustitutas de Comida", "Snacks Proteicos"],
        "Listo para Beber" : ["Listo para Beber"],
        "Hidratos de Carbono" : ["Hidratos de Carbono","Carbohidratos"],
        "Intraentrenamiento" : ["Intraentrenamiento", "Pump", "Intra-Entrenamiento"],
        "Recuperación Posentrenamiento" : ["Recuperación Posentrenamiento", "Recover & Refuel", "Post-Entrenamiento y Recuperación"],
        "Creatina" : ["Creatina"],
        "BCAA" : ["BCAA", "BCAA's (Aminoácidos Ramificados)"],
        "EAA (Aminoácidos Esenciales)" : ["EAA (Aminoácidos Esenciales)", "EAA's (Aminoácidos Esenciales)"],
        "Glutamina" : ["Glutamina"],
        "Aminoácidos": ["Aminoácidos Aislados", "HMB", "Aminoácidos"],
        "Estimulantes de Testosterona" : ["Estimulantes de Testosterona", "Test Boosters", "Pro-Testosterona", "ZMA", "Precursores de la Testosterona"],
        "Cafeína" : ["Cafeína"],
        "L-Carnitina" : ["L-Carnitina"],
        "Energy Series" : ["Energy Series"],
        "Barritas Energéticas" : ["Barritas Energéticas"],
        "Geles Energéticos" : ["Geles Energéticos"],
        "Bebidas Energéticas" : ["Bebidas Energéticas"],
        "Bebidas Isotónicas/Con electrolitos" : ["Bebidas Isotónicas/Con electrolitos"],
        "Termogénicos" : ["Termogénicos", "Fat Burners", "Quemadores termogénicos", "Quemadores"],
        "Quemadores de Grasa sin Estimulantes" : ["Quemadores de Grasa sin Estimulantes", "Quemadores termogénicos sin estimulantes"] ,
        "Cremas Quemagrasas" : ["Cremas Quemagrasas", "Cremas Reductoras"],
        "CLA" : ["CLA"],
        "Bloqueadores de Carbohidratos" : ["Bloqueadores de Carbohidratos", "Bloqueadores Grasas y/o Carbohidratos"],
        "Control del Apetito" : ["Control del Apetito"],
        "Diuréticos y Depurativos" : ["Diuréticos y Depurativos", "Diuréticos"],
        "Productos Zero y Dietéticos" : ["Productos Zero y Dietéticos", "Sustitutas de Comida"],
        "Vitaminas y Minerales" : ["Vitaminas y Minerales", "Minerales", "Multivitamínicos", "Vitaminas", "Micronutrientes"],
        "Articulaciones, Cartílagos y Huesos" : ["Articulaciones, Cartílagos y Huesos"],
        "Antioxidantes y Hierbas" : ["Antioxidantes y Hierbas"],
        "Ómega 3 y Otros Ácidos Grasos" : ["Ómega 3 y Otros Ácidos Grasos"],
        "Hígado y Depurativos" : ["Hígado y Depurativos"],
        "Prohormonales" : ["Prohormonales", "Control/Reducir Cortisol", "Control/Reducir Estrógenos","Pro-Hormona Crecimiento"] 
    }


mapeo_categorias = {
        "Proteina" : ["Proteína Whey", "Aislado de Whey y Whey Nativa", "Hidrolizado de Proteína Whey", "Caseína e Proteína de liberación lenta", "Proteína de Huevo y de Carne", "Ganadores de Masa", "Proteína Vegetal", "Colágeno", "Proteína Dietética", "Barritas Proteicas", "Snacks Proteicos", "Alimentación Proteica", "Listo para Beber"],
        "Desarrollo Muscular" : ["Proteína Whey","Aislado de Whey y Whey Nativa","Ganadores de Masa","Hidratos de Carbono","Preentrenamiento y Óxido Nítrico", "Intraentrenamiento", "Recuperación Posentrenamiento", "Creatina", "BCAA", "EAA (Aminoácidos Esenciales)", "Glutamina", "Aminoácidos", "Estimulantes de Testosterona"],
        "Energía y resistencia" : ["Preentrenamiento y Óxido Nítrico","Intraentrenamiento","Recuperación Posentrenamiento","Cafeína","Creatina","BCAA","L-Carnitina","Energy Series","Barritas Energéticas", "Geles Energéticos", "Bebidas Energéticas", "Bebidas Isotónicas/Con electrolitos","Hidratos de Carbono"],
        "Quemadores de grasa y definición" : ["Termogénicos", "Quemadores de Grasa sin Estimulantes", "Cremas Quemagrasas", "CLA","L-Carnitina", "Bloqueadores de Carbohidratos", "Control del Apetito", "Diuréticos y Depurativos","Proteína Dietética", "Productos Zero y Dietéticos"],
        "Salud del Atleta" : ["Vitaminas y Minerales", "Articulaciones, Cartílagos y Huesos", "Antioxidantes y Hierbas", "Ómega 3 y Otros Ácidos Grasos", "Hígado y Depurativos", "Prohormonales"]
    }

def populate_categorias():
    categorias = ["Proteina", "Desarrollo Muscular", "Energía y resistencia", "Quemadores de grasa y definición", "Salud del Atleta"]
    for nombre in categorias:
        existe_registro = Categoria.objects.filter(nombre=nombre).exists()
        if not existe_registro:
            Categoria.objects.create(nombre=nombre)
        else:
            print(f"Registro duplicado: {nombre}")

def asignar_categoria(subcategoria):
    for categoria, subcategorias in mapeo_categorias.items():
        if subcategoria in subcategorias:
            return categoria
    return "No categoria asignada"


def asignar_subcategoria(subcategoria_scrapeada):
    for subcategoria, equivalentes in mapeo_subcategorias.items():
        if subcategoria_scrapeada in equivalentes:
            return subcategoria  
    return "No subcategoria asignada"

def get_imagen_hsn(url):
    req = Request(url = url, headers=headers)
    with urlopen(req) as response, open('temp.jpg', 'wb') as imagen_temp:
        imagen_temp.write(response.read())

def get_sabores_hsn(url, driver):
    driver.get(url)
    sabores = []
    try:
        sabores_aux = driver.find_element(By.CLASS_NAME, "product_view_Sabor")
        for s in sabores_aux.find_elements(By.TAG_NAME, "option"):
            sabores.append(s.text.strip())
    except:
        sabores.append("Sabor único") 
    time.sleep(2)
    return sabores
    
def parse_ingredientes(ingredientes):
    # Utilizar una expresión regular para encontrar elementos fuera de paréntesis
    elementos_fuera = re.findall(r'[^,(]+(?:\([^)]*\)[^,(]*)*', ingredientes)
    # Dividir cada elemento encontrado por comas
    resultado = [elemento.strip() for elemento in elementos_fuera if elemento.strip()]
    resultado_limpio = []
    for elemento in resultado:
        soup = BeautifulSoup(elemento, 'html.parser')
        texto_limpio = soup.get_text()
        resultado_limpio.append(texto_limpio)

    return resultado_limpio

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

def get_reviews_big(url, driver):
    driver.get(url)
    time.sleep(3)
    reviews = []
    try:
        reviews_tab = driver.find_element(By.XPATH, "//a[contains(@href, '#tab-3')]")
    except NoSuchElementException:
        try:
            reviews_tab = driver.find_element(By.XPATH, "//li[contains(@class, 'tab') and contains(.,'Reviews')]")
        except NoSuchElementException:
            return "No hay reviews"
    driver.execute_script("arguments[0].click();", reviews_tab)
    time.sleep(3)
    try:
        reviews_element = driver.find_elements(By.XPATH, "//div[contains(@class, 'content-review')]")
        for r in reviews_element:
            review = r.text
            reviews.append(review)
    except:
        reviews = "Sin reviews"

    
    reviews = list(filter(None, reviews))
    return reviews

def get_descripcion_big(s):
    descripcion_final = ""
    try:
        descripcion_div = s.find("section", id="product_description")
        descripcion = descripcion_div.find_all("p")
        descripcion_text = " ".join(str(e.text.strip()) for e in descripcion)
        # Reemplaza múltiples espacios en blanco con un solo espacio
        descripcion_final = re.sub(r'\s+', ' ', descripcion_text)
    except:
        try:
            descripcion = s.find("div", id="tab-1").find_all("p")
            descripcion_final = " ".join(str(e.text.strip()) for e in descripcion)
        except:
            descripcion_div = s.find("div", class_="short-description")
            descripcion_final = descripcion_div.text.strip()
    return descripcion_final


def get_ingredientes_big(url, driver):
    driver.get(url)
    ingredientes = []
    time.sleep(3)
    try:
        info_nutricional = driver.find_element(By.XPATH, "//a[contains(@href, '#tab-2')]")
    except NoSuchElementException:
        try:
            info_nutricional = driver.find_element(By.XPATH, "//li[contains(@class, 'tab') and contains(.,'Info. Nutricional')]")
        except NoSuchElementException:
            ingredientes.append("Sin ingredientes")
            return ingredientes
    
    driver.execute_script("arguments[0].click();", info_nutricional)
    time.sleep(3)
    try:
        ingredientes_element = driver.find_element(By.CSS_SELECTOR, "table.nutri_info").find_element(By.XPATH, "//p[starts-with(normalize-space(), 'Ingredientes')][1]")

        # Omitir elementos en etiquetas <b>
        ingredientes_texto = ingredientes_element.get_attribute("innerHTML")
        ingredientes_sin_etiquetas_b = re.sub(r'<(strong|b)>(.*?)</(strong|b)>', '', ingredientes_texto)

        ingredientes = ingredientes_sin_etiquetas_b.strip()
        if ingredientes.startswith(":"):
            ingredientes = ingredientes[1:].strip()
        
    except NoSuchElementException:
        ingredientes.append("Sin ingredientes")
        return ingredientes

    ingredientes = parse_ingredientes(ingredientes)
    return ingredientes

def get_sabores_big(url, driver):
    driver.get(url)
    time.sleep(2)
    sabores = []
    try:
        sabores_aux = driver.find_element(By.ID, "option-sabor")
    except NoSuchElementException:
        try:
            sabores_aux = driver.find_element(By.ID, "option-flavour")
        except NoSuchElementException:
            sabores.append("Sabor único")
            return sabores

    for s in sabores_aux.find_elements(By.TAG_NAME, "option"):
        if s.text.strip():  # Esto evitará agregar opciones vacías
            sabores.append(s.text.strip())

    time.sleep(2)
    return sabores

def get_imagen_big(url):
    req = Request(url = url, headers=headers)
    with urlopen(req) as response, open('temp.jpg', 'wb') as imagen_temp:
        imagen_temp.write(response.read())

def get_rating_big(url, driver):
    driver.get(url)
    time.sleep(3)
    try:
        rating = driver.find_element(By.CLASS_NAME, "sr-only").text.split(" ")[0]
    except:
        rating = 0.0
    return rating

def get_imagen_prozis(url):
    req = Request(url = url, headers=headers)
    with urlopen(req) as response, open('temp.jpg', 'wb') as imagen_temp:
        imagen_temp.write(response.read())








