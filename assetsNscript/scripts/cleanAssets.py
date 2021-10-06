#!/usr/bin/python3.9

from os import remove, getcwd, listdir
from os.path import split, exists

# bsucando y obteniendo path
print('buscando directory')
seed_path = getcwd()
dst = split(seed_path)
dst = dst[0] + '/' + 'assetsNscript/assets'

# obteniendo lista para borar
if exists(dst):
    remove_list = listdir(dst)
else:
    print('Directory dont exists')

# borrar lista
print('borrando items')
for item in remove_list:
    remove(dst + '/' + item)
