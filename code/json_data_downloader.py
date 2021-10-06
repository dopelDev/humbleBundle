#!/usr/bin/python3.8

from bs4 import BeautifulSoup
from json import dump, loads, load
from subprocess import call
# scrappy 

# obterner el json del html
def load_data(path : str):
    work_directory = path 
    obj_file = open(work_directory + '/assetsNscript/assets/humbleBundle.html', mode='r')
    soup = BeautifulSoup(obj_file.read(), 'html.parser')
    data = soup.find_all('script', {'id':{'landingPage-json-data'}})
    return data

# function para remover el tag
def remove_tag(ResultSet):
    dirty_text = str(ResultSet)
    cutString = ''
    print('la lenght de dirty text : ', len(dirty_text))
    count = 0
    for index, item in enumerate(dirty_text):
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

# function para guardar el json sin tag
def save_json(clean_text : str, path : str):
    work_directory = path
    json = loads(clean_text)
    obj_file = open(work_directory + '/cleanData/pretty.json', mode='w')
    dump(json, obj_file, indent=2)

def load_decode_json(path : str):
    work_directory = path 
    obj_file = open(work_directory + '/cleanData/pretty.json', mode='r')
    json_file = load(obj_file)
    obj_file.close()
    print(type(json_file))
    return json_file 

# call al script de download
def download_html(path : str):
    call(['python', path + '/assetsNscript/scripts/download.py']) 

def cleanAssets(path : str):
    call(['python', path + '/assetsNscript/scripts/cleanAssets.py']) 


def searcher(data):
    pass
