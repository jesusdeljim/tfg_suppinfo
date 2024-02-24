from main.utils.imports import *
from main.utils.utils import *
from main.scrapping import raw_nutrition_scrapping, hsn_store_scrapping, big_supplementation_scrapping, prozis_scrapping


def populate():
    print("Populating database...")
    writer = ix.writer()
    driver = getGeckoDriver()
    print("Populating categories...")
    populate_categorias()
    print("Categories populated successfully")
    print("Populating products...")
    hsn_store_scrapping.hsn_scrap(driver, writer)
    prozis_scrapping.prozis_scrap(driver, writer)
    big_supplementation_scrapping.big_scrap(driver, writer)
    raw_nutrition_scrapping.raw_scrap(driver, writer)
    driver.quit()
    writer.commit()
    print("Se han cargado " +str(ix.searcher().doc_count()) + " descripciones y reviews")
    print("Populating finished successfully")
    
    
