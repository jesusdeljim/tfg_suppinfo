from main.utils.imports import *
from main.utils.utils import *
from main.scrapping import raw_nutrition_scrapping, hsn_store_scrapping, big_supplementation_scrapping, prozis_scrapping
import time

dirindex="Index"

def populate():
    sch = Schema(id_producto=ID(stored=True),nombre=TEXT(stored=True), descripcion=TEXT(stored=True), reviews=TEXT(stored=True))
    ix = create_in(dirindex, schema=sch)
    print("Populating database...")
    writer = ix.writer()
    driver = getGeckoDriver()
    print("Populating categories...")
    populate_categorias()
    print("Categories populated successfully")
    print("Populating products...")
    
    start_time = time.time()
    
    hsn_store_scrapping.hsn_scrap(driver, writer)
    prozis_scrapping.prozis_scrap(driver, writer)
    big_supplementation_scrapping.big_scrap(driver, writer)
    raw_nutrition_scrapping.raw_scrap(driver, writer)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    driver.quit()
    writer.commit()
    print("Se han cargado " + str(Producto.objects.all().count()) + " productos")
    print("Se han cargado " +str(ix.searcher().doc_count()) + " descripciones y reviews")
    print("Populating finished successfully")
    print("Elapsed time: " + str(elapsed_time) + " seconds")

    return Producto.objects.all().count()

    
