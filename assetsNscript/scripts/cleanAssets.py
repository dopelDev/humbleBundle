#!/usr/bin/python3.8

from os import remove, getcwd, listdir
from os.path import split, exists

# bsucando y obteniendo path
print('buscando directory')
seed_path = getcwd()
dst = split(seed_path)
dst = dst[0] + '/' + 'assets'

# obteniendo lista para borar
if exists(dst):
    remove_list = listdir(dst)
else:
    print('Directory dont exists')

# borrar lista
for item in remove_list:
    remove(dst + '/' + item)
