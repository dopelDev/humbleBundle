from requests import get
from bs4 import BeautifulSoup
from json import loads
from typing import Dict, Tuple, List

def get_json():

    """
        obtiene el tag de java_script_content 
        remueve el tag con remove_tag
        retorna un Objeto json
    """

    URL = 'https://www.humbleBundle.com/books'
    html = get(URL)
    sopa = BeautifulSoup(html.text, 'html.parser')
    java_script_content = sopa.find_all('script', {'id':{'landingPage-json-data'}})
    clean_data = remove_tag(java_script_content)

    return loads(clean_data) 


def remove_tag(java_script_content):
    dirty_text = str(java_script_content)
    cutString : str = ''
    count = 0
    for item in dirty_text:
        if item == '>':
            cutString += item
            count += 1
            break
        else:
            cutString += item
            count += 1
    # 10 chars porque </scripts>
    clean_text = dirty_text[count:-10]
    return clean_text 


def get_content(obj_json : Dict) -> Tuple[List, List]:
    header =  obj_json.get('data').get('books').get('mosaic')[0].get('products')[0].keys()
    content = obj_json.get('data').get('books').get('mosaic')[0].get('products')

    return (header, content)
