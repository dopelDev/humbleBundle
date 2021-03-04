#!/usr/bin/python3.8

from json import load
from pprint import pprint

obj_file = open('/home/dopel/codeInTest/humbleBundle/cleanData/text.json', mode='r')
obj_json = load(obj_file)

print('Main'.center(100, '='))

for key in obj_json:
    print(key)

print('data'.center(100, '='))

for key in obj_json['data']:
    print(key)

print('books'.center(100, '='))

for key in obj_json['data']['books']:
    print(key)
    
print('mosaic'.center(100, '='))
print(type(obj_json['data']['books']['mosaic']))
print('lenght of mosaic : ' , len(obj_json['data']['books']['mosaic']))
print('copiando mosaic')
mosaic = obj_json['data']['books']['mosaic'][0]
print(type(mosaic))

print('new mosaic'.center(100, '='))
for key in mosaic:
    print(key)

print('products'.center(100, '='))
print(type(mosaic['products']))
#for key in mosaic['products']:
#    print(key)

