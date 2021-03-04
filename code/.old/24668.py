#!/usr/bin/python3.8

from bs4 import BeautifulSoup
from time import sleep
from pprint import pprint
from json import JSONDecoder, JSONEncoder, loads, load 
from tempfile import TemporaryFile

# scrappy 

work_directory = '/home/dopel/codeInTest/humbleBundle'
obj_file = open(work_directory + '/assetsNscript/assets/humbleBundle.html', mode='r')
soup = BeautifulSoup(obj_file.read(), 'html.parser')
data = soup.find_all('script', {'id':{'landingPage-json-data'}})

str_data = str(data).replace(',', ', \n')
# str_data = str(data) 
# print(str_data)
str_line_data = list(str_data.split('\n'))

# for line, text in enumerate(str_line_data):
#   print('{} : \n{}'.format(line, text))

obj_file = open('/home/dopel/codeInTest/humbleBundle/assetsNscript/assets/text.json', mode='w')

for line in str_line_data:
    obj_file.writelines(line)

obj_file.close()
