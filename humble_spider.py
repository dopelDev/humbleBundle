import sys
from requests import get, exceptions
from bs4 import BeautifulSoup
from json import loads
from typing import Dict, Tuple, List
from pandas import DataFrame, json_normalize

def get_json() -> Dict:

    """
        obtiene el tag de java_script_content 
        remueve el tag con remove_tag
        retorna un Objeto json
    """

    URL = 'https://www.humbleBundle.com/books'

    try:
        response = get(URL)
        response.raise_for_status()
    except exceptions.RequestException as e:
        print(f'Error no se obtuvo respuesta 200 GET : {e}')
        sys.exit()

    sopa = BeautifulSoup(response.text, 'html.parser')
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


def get_content(object_json : Dict) -> DataFrame:
    content = object_json.get('data').get('books').get('mosaic')[0].get('products')

    return json_normalize((content))
