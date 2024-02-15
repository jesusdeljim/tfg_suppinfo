from .imports import *

mapeo_subcategorias = {
        "Preentrenamiento y Óxido Nítrico": ["Pre-Workout", "Pre-entreno", "Preentrenamiento", "Preentrenamiento y Óxido Nítrico", "óxido nítrico", "Pre-Entrenamiento", "Suplementos Pre-Entreno", "Pre-entrenos"],
        "Proteína Whey" : ["Protein", "Proteínas", "Batidos de proteínas en Polvo", "Proteínas Aisladas de Suero", "Proteínas Concentradas de Suero"],
        "Aislado de Whey y Whey Nativa" : ["Protein", "Proteínas", "Batidos de proteínas en Polvo", "Proteínas Aisladas de Suero", "Proteínas Concentradas de Suero"],
        "Hidrolizado de Proteína Whey" : ["Proteínas Hidrolizadas"],
        "Caseína e Proteína de liberación lenta" : ["Caseínas", "Proteínas Liberación Secuencial"],
        "Proteína de Huevo y de Carne" : ["Proteínas de Albúmina de Huevo", "Proteínas de Carne"],
        "Ganadores de Masa" : ["Ganadores de Peso"],
        "Proteína Vegetal" : ["Proteínas Vegetales"],
        "Colágeno" : [],
        "Proteína Dietética" : [],
        "Barritas Proteicas" : ["Barritas de Proteínas", "Snacks Proteicos"],
        "Snacks Proteicos" : ["Barritas de Proteínas", "Sustitutas de Comida", "Snacks Proteicos"],
        "Alimentación Proteica" : ["Barritas de Proteínas", "Sustitutas de Comida", "Snacks Proteicos"],
        "Listo para Beber" : [],
        "Hidratos de Carbono" : ["Carbohidratos"],
        "Intraentrenamiento" : ["Pump", "Intra-Entrenamiento"],
        "Recuperación Posentrenamiento" : ["Recover & Refuel", "Post-Entrenamiento y Recuperación"],
        "Creatina" : ["Creatina"],
        "BCAA" : ["BCAA's (Aminoácidos Ramificados)"],
        "EAA (Aminoácidos Esenciales)" : ["EAA's (Aminoácidos Esenciales)"],
        "Glutamina" : ["Glutamina"],
        "Aminoácidos": ["Aminoácidos Aislados", "HMB", "Aminoácidos"],
        "Estimulantes de Testosterona" : ["Test Boosters", "Pro-Testosterona", "ZMA", "Precursores de la Testosterona"],
        "Cafeína" : [],
        "L-Carnitina" : [],
        "Energy Series" : [],
        "Barritas Energéticas" : ["Barritas Energéticas"],
        "Geles Energéticos" : [],
        "Bebidas Energéticas" : [],
        "Bebidas Isotónicas/Con electrolitos" : [],
        "Termogénicos" : ["Fat Burners", "Quemadores termogénicos", "Quemadores"],
        "Quemadores de Grasa sin Estimulantes" : ["Quemadores termogénicos sin estimulantes"] ,
        "Cremas Quemagrasas" : ["Cremas Reductoras"],
        "CLA" : [],
        "Bloqueadores de Carbohidratos" : ["Bloqueadores Grasas y/o Carbohidratos"],
        "Control del Apetito" : ["Control del Apetito"],
        "Diuréticos y Depurativos" : ["Diuréticos"],
        "Productos Zero y Dietéticos" : ["Sustitutas de Comida"],
        "Vitaminas y Minerales" : ["Minerales", "Multivitamínicos", "Vitaminas", "Micronutrientes"],
        "Articulaciones, Cartílagos y Huesos" : [],
        "Antioxidantes y Hierbas" : [],
        "Ómega 3 y Otros Ácidos Grasos" : [],
        "Hígado y Depurativos" : [],
        "Prohormonales" : ["Control/Reducir Cortisol", "Control/Reducir Estrógenos","Pro-Hormona Crecimiento"] 
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
    return None


def asignar_subcategoria(subcategoria_scrapeada):
    for subcategoria, equivalentes in mapeo_subcategorias.items():
        if subcategoria_scrapeada in equivalentes:
            return subcategoria
    return subcategoria_scrapeada

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