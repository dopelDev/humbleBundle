#!/usr/bin/python3.9
# script para bajar el html

#imports
from os import getcwd, mkdir
from os.path import split, exists
from requests import get

seed_path = getcwd()
dst = split(seed_path)
dst = dst[0] + '/' + 'assetsNscript/assets'
print('buscando directory')

def recurse_download():
    if exists(dst):
        print('existe el directory\nDescango..')
        html = get('https://www.humblebundle.com/books') 
        objFile = open(dst + '/' + 'humbleBundle.html', mode='w')
        objFile.write(html.text)
    else:
        print('directory dont exists\nCreando directory')
        mkdir(dst)
        recurse_download()
recurse_download()
print('descargado')
