from .scrapping import raw_nutrition_scrapping
from .scrapping import my_protein_scrapping
from .scrapping import big_supplementation_scrapping
from .scrapping import prozis_scrapping
from .scrapping import hsn_store_scrapping
from .utils.utils import *

def populate():
    populate_categorias()
    raw_nutrition_scrapping.raw_scrap()
    #hsn_store_scrapping.hsn_scrap()
    
