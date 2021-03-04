#!/usr/bin/python3.8

from json import loads, load
from pprint import pprint

path = '/home/dopel/codeInTest/humbleBundle/assetsNscript/assets/text.json'
obj_file = open(path, mode='r')
data = obj_file.read()
obj_file.close()
obj_json = loads(data)
#pprint(obj_json[data])

for key in obj_json:
    print(key)
