#from ..utils.imports import *
#from ..utils.utils import *

import os
import random
import sys
from bs4 import BeautifulSoup
import bs4
import urllib.request
from urllib.error import HTTPError
from urllib.request import urlopen, Request
import lxml
import re
import ssl
import time
from datetime import datetime

from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD, ID
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from whoosh.query import And

from django.db import IntegrityError
from django.core.files import File

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

def getGeckoDriver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    firefox_options = Options()
    #firefox_options.add_argument("--headless")
    firefox_options.set_preference('general.useragent.override', user_agent)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    return driver

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


def prozis_scrap(driver):
    driver.get(url_prozis)   
    time.sleep(2)
    driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click() 
    num_pags = driver.find_elements(By.CLASS_NAME, "pagination-button")[-2].text
    urls_productos = []
    for pag in range(1, 2): #int(num_pags)+1
        driver.get(url_prozis + f"/q/page/{pag}")
        time.sleep(2)
        productos = driver.find_element(By.CLASS_NAME, "row.list-container").find_elements(By.CLASS_NAME, "col.list-item")
        for producto in productos:
            url_producto = producto.find_element(By.TAG_NAME, "a").get_attribute("href")
            urls_productos.append(url_producto)
    
    for url_producto in urls_productos:
        driver.get(url_producto)
        time.sleep(2)
        subcategoria_scrapeada = driver.find_element(By.ID, "breadcrumbs").find_elements(By.TAG_NAME, "a")[-2].text
        #subcat = asignar_subcategoria(subcategoria_scrapeada)
        #if subcat == "No subcategoria asignada":
        #    continue
        #cat = asignar_categoria(subcat)
        #categoria = Categoria.objects.get_or_create(nombre = cat)[0] 
        #subcategoria = Subcategoria.objects.get_or_create(nombre = subcat, categoria = categoria)[0]
        nombre = driver.find_element(By.ID, "breadcrumbs").find_elements(By.TAG_NAME, "a")[-1].text
        precio = driver.find_element(By.XPATH, "//p[@class='final-price']").get_attribute("data-qa").replace("€", "").replace(",",".").strip()
        marca = "PROZIS"
        #brand = Marca.objects.get_or_create(nombre = marca)[0]
        rating = driver.find_element(By.CLASS_NAME, "prz-blk-content-rating").find_element(By.TAG_NAME, "span").text.split("/")[0].strip()
        stock = True
        stock_div = driver.find_element(By.CLASS_NAME, "stock-info").text.strip()
        if "No disponible" in stock_div:
            stock = False
        else:
            stock = True
        
        url_imagen = driver.find_element(By.CLASS_NAME, "first-column").find_element(By.TAG_NAME, "img").get_attribute("src")
        #get_imagen_prozis(url_imagen)

        sabores = []
        ingredientes = []
        driver.find_element(By.CLASS_NAME, "prz-blk-content").click() #Abre menu info nutricional para coger sabores e ingredientes.
        time.sleep(2)
        try:
            driver.find_element(By.CLASS_NAME, "nut-tbl-select-box").click()
            for sabor in driver.find_elements(By.TAG_NAME, "li"):
                sabores.append(sabor.text)
            
        except NoSuchElementException:
            sabores.append("Sabor único")
        sabores = list(filter(None, sabores))
        ingredientes_text = driver.find_element(By.CLASS_NAME, "nut-other-ingredients").find_element(By.CLASS_NAME, "list").text
        ingredientes_text = ingredientes_text[:-1]
        ingredientes = parse_ingredientes(ingredientes_text)
        driver.find_element(By.ID, "contentCloseBtn").click() #Cierra menu info nutricional
        time.sleep(1)
        #Buscamos de nuevo el elemento "prz-blk-content", pero en vez de coger el primero cogemos el siguiente, que sera el de las reviews
        driver.find_elements(By.CLASS_NAME, "prz-blk-content")[1].click()
        time.sleep(2)
        reviews_divs = driver.find_element(By.CLASS_NAME, "reviews-section.customer-reviews").find_elements(By.CLASS_NAME, "review-detailed")
        reviews_list=[]
        for review in reviews_divs:
            reviews_list.append(review.find_element(By.CLASS_NAME, "review-content").text)

        reviews = "|writer_split|".join(str(e) for e in reviews_list)
        
        driver.find_element(By.ID, "contentCloseBtn").click() #Cierra menu reviews
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "prz-blk-content.pdp-block-horizontal.prz-blk-content-with-img").click() #Abre menu descripciones
        time.sleep(2)
        
        
        print("NUEVO PRODUCTO:\n")
        print(nombre, url_producto, subcategoria_scrapeada, precio, marca, rating, stock)
        print(sabores)
        print(ingredientes)
        print(reviews)
        print("---------------------------------------------------------------\n")

    
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

if __name__ == '__main__':
    driver = getGeckoDriver()
    prozis_scrap(driver)
    driver.close()
    print("Prozis Scraping finished")
    print("Indexing finished")