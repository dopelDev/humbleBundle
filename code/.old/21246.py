#!/usr/bin/python3.8

from bs4 import BeautifulSoup
from os import getcwd
import re
from time import sleep
from pprint import pprint

# keywords
keywords = ['HUMBLE BOOKS BUNDLE', 'UNF*CK YOUR LIFE BY MICROCOSM',
'SURVIVE EVERYTHING BY SKYHORSE','FALLOUT RPG & 3D MINIATURES BY MODIPHIUS',
'MOEBIUS & MORE PRESENTED BY HUMANOIDS','BECOME AN ENTREPRENEUR BY WILEY',
'ASTRONOMY, BLACK HOLES & THE UNIVERSE BY MORGAN & CLAYPOOL',
'title']

keywords2 = []

for key in keywords:
    tmp = (key.split(' '))
    for item in tmp:
        keywords2.append(item)
# scrappy 

work_directory = '/home/dopel/codeInTest/humbleBundle'
obj_file = open(work_directory + '/assetsNscript/assets/humbleBundle.html', mode='r')
soup = BeautifulSoup(obj_file.read(), 'html.parser')
data = soup.find_all('script', {'id':{'landingPage-json-data'}})
str_data = str(data)
list_data = list(str_data.split("]"))
print(len(list_data)) #257
len_list_data = []
for item in list_data:
    len_list_data.append(len(item))
print(len_list_data)
sleep(2)

for item in list_data:
    for key in keywords2:
        if key in item or key.lower() in item:
            print('Found key : ' + key)
            print(item)
            sleep(0.02)
        elif key is keywords[-1]:
            print('Found any keys')
            sleep(0.02)
        else:
            print('no found key')
            sleep(0.02)
