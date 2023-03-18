import sys
from requests import get, exceptions
from bs4 import BeautifulSoup
from typing import Dict
import pandas as pd
from json import loads

"""
    obtiene el tag de java_script_content 
    remueve el tag con remove_tag
    retorna un Objeto json serializado
"""

class HumbleSpider:

    def __init__(self):
        self.URL = 'https://www.humbleBundle.com/books'
        self.json_object = self.get_json()
        self.content = self.get_content(self.json_object)

    def get_json(self) -> Dict:
        try:
            response = get(self.URL)
            response.raise_for_status()
        except exceptions.RequestException as e:
            print(f'Error no se obtuvo respuesta 200 GET : {e}')
            sys.exit()

        sopa = BeautifulSoup(response.text, 'html.parser')
        java_script_content = sopa.find_all('script', {'id':{'landingPage-json-data'}})
        clean_data = self.remove_tag(java_script_content)
        return loads(clean_data) 

    def remove_tag(self, java_script_content):
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
        # 10 chars dub </scripts>
        clean_text = dirty_text[count:-10]
        return clean_text 

    def get_content(self, object_json : Dict) -> pd.DataFrame:
        content = object_json.get('data').get('books').get('mosaic')[0].get('products')
        return pd.json_normalize(content)

    def get_urls(self) -> list:
        urls_second_part = self.content['product_url'].tolist()
        urls_first_part = 'https://www.humblebundle.com'
        urls = [str]
        for url in urls_second_part:
            url = urls_first_part + url
            urls.append(url)
        return urls
