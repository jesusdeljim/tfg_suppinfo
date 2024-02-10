from ..utils.imports import *


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url_big = "https://bigsupps.site"

def big_scrap_categorias():
    f = urllib.request.urlopen(str(url_big))
    s = BeautifulSoup(f,"lxml")
    cats = s.find("ul",class_="megamenu_ul has-text-white").find_all("li")
    categorias = []
    for e in cats:
        categorias.append(e.text.strip())
        categorias = categorias[0:7]
    print(categorias)

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