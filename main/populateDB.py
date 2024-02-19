from .scrapping import raw_nutrition_scrapping
from .scrapping import my_protein_scrapping
from .scrapping import big_supplementation_scrapping
from .scrapping import prozis_scrapping
from .scrapping import hsn_store_scrapping
from .utils.utils import *
from .utils.imports import *

def populate():
    print("Populating database...")
    writer = ix.writer()
    driver = getGeckoDriver()
    populate_categorias()
    raw_nutrition_scrapping.raw_scrap(driver, writer)
    hsn_store_scrapping.hsn_scrap(driver, writer)
    big_supplementation_scrapping.big_scrap(driver, writer)
    prozis_scrapping.prozis_scrap(driver, writer)
    driver.quit()
    writer.commit()
    print("Populating finished successfully")
    
    
