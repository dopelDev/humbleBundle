#!/usr/bin/python3.8

from bs4 import BeautifulSoup
from os import getcwd
import re
from time import sleep
from pprint import pprint
from json import JSONDecoder, JSONEncoder, loads 

# scrappy 

work_directory = '/home/dopel/codeInTest/humbleBundle'
obj_file = open(work_directory + '/assetsNscript/assets/humbleBundle.html', mode='r')
soup = BeautifulSoup(obj_file.read(), 'html.parser')
data = soup.find_all('script', {'id':{'landingPage-json-data'}})

# keywords
words_before = [',', ':']
words_after = [', \n', ': \n']
length = len(words_before)
str_data = str(data)

str_re = str_data.replace(words_before[0],words_after[0])
str_re = str_re.replace(words_before[1],words_after[1])
str_re.encode('utf-8')
list_str_re = list(str_re.split(']'))

# print(str_re)
# print(loads(str_re))
print(len(list_str_re))
for index,item in enumerate(list_str_re):
    print('item numer : ', index)
    print(item)
    sleep(0.5)
