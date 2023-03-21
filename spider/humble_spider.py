import sys
from requests import get, exceptions
from bs4 import BeautifulSoup
from typing import Dict
import pandas as pd
from json import loads

"""
    create a spider to get the json object from humble bundle
    first step  get_json : get a json object
    second step remove_tag : remove the tag from the json object
    third step  get_content : return a pandas dataframe with the content of the json object serialized with pandas json_normalize
"""

class HumbleSpider:

    """
        self.content is a raw json object
    """

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

    """
        return a pandas dataframe with the content of the json object
    """

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

"""
    create a new spider and get the bundles information
    
    class BundleSpider(): get a list of urls and get the information of each bundle
    def get_raw_data_bundle(self, List[str]) -> tbd
"""

