import os
from bs4 import BeautifulSoup
import bs4
import urllib.request
from urllib.error import HTTPError
from urllib.request import urlopen
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

from main.models import Marca, Producto, Sabor, Ingrediente, Proteina, Vitamina, Snack, Categoria


def getGeckoDriver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    firefox_options = Options()
    firefox_options.set_preference('general.useragent.override', user_agent)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    return driver