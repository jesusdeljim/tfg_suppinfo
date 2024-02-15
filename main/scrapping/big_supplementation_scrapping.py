#from ..utils.imports import *
#from ..utils.utils import *

import os
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

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url_big = "https://bigsupps.site"

def big_scrap_aminoacidos():
    url_amino = str(url_big)+"/collections/aminoacids"
    for pag in range(1,3):
        f = urllib.request.urlopen(str(url_amino)+"?page="+str(pag))
        s = BeautifulSoup(f, "lxml")
        aminoList = s.find("div", class_="product-list").find_all("div", class_="product-block detail-mode-permanent fixed-width")
        for p in aminoList:
            amino_url = p.find("a", class_="product-link")['href']
            f = urllib.request.urlopen(str(url_big)+str(amino_url))
            s = BeautifulSoup(f, "lxml")
            amino_nombre = s.find("h1", class_="title").text.strip()
            amino_precio = s.find("div", class_="price-text after").find("span").text
            amino_img_url = p.find("img", class_="rimage__image fade-in lazyautosizes lazyloaded")
            print(amino_img_url)


def big_scrap():
    big_scrap_categorias()
    big_scrap_aminoacidos()

#main method to execute the scrapping
if __name__ == "__main__":
    big_scrap()