from ..utils.imports import *

if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
    ssl, "_create_unverified_context", None
):
    ssl._create_default_https_context = ssl._create_unverified_context

url_mp = "https://www.myprotein.es"


def myprotein_scrap_categories():
    f = urllib.request.urlopen(str(url_mp))
    s = BeautifulSoup(f, "lxml")
    categorias = s.find("div", class_="responsiveFlyoutMenu_mobilePanelContainer").find(
        "li", class_="responsiveFlyoutMenu_levelOneItem-slide"
    )
    print(categorias)


def myprotein_scrap_proteins():
    # scrapping de la seccion de proteina
    url_proteina = str(url_mp) + "/nutrition/protein.list"
    for pag in range(1, 4):
        f = urllib.request.urlopen(str(url_proteina) + "?pageNumber=" + str(pag))
        s = BeautifulSoup(f, "lxml")
        products_list = s.find("ul", class_="productListProducts_products").find_all(
            "li"
        )
        for product in products_list:
            product_url = product.find("a", class_="athenaProductBlock_linkImage")[
                "href"
            ]
            f = urllib.request.urlopen(str(url_mp) + str(product_url))
            s = BeautifulSoup(f, "lxml")
            url_imagen = s.find("img", class_="athenaProductImageCarousel_image")["src"]
            product_name = s.find("h1", class_="productName_title").text
            flavours_aux = s.find("select", class_="athenaProductVariations_dropdown")
            flavours_list = []
            if flavours_aux == None:
                flavours_list.append("Sin sabor")
            else:
                flavours = flavours_aux.find_all("option")
                for flavour in flavours:
                    flavours_list.append(flavour.text.strip())


def mp_scrap():
    myprotein_scrap_categories()
    myprotein_scrap_proteins()
