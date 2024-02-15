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

import importlib
import inspect
from main.models import Marca, Producto, Sabor, Ingrediente, Proteina, Vitamina, Snack, Categoria, Subcategoria

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

dirindex="Index"

sch = Schema(id_producto=ID(stored=True),nombre=TEXT(stored=True), descripcion=TEXT(stored=True), reviews=TEXT(stored=True))
ix = create_in(dirindex, schema=sch)


def getGeckoDriver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.set_preference('general.useragent.override', user_agent)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    return driver