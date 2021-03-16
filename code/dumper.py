from json import dumps, load
from os.path import split
from os import getcwd

path = getcwd()
path_list = split(path)
workdir = path_list[0] + '/cleanData'

obj_file = open(workdir + '/text.json', mode='r')
obj_json = load(obj_file)
obj_file.close()
obj_file = open(workdir + '/pretty.json', mode='w')
obj_file.write(dumps(obj_json, indent=4))
obj_file.close()
