#!/usr/bin/python3.8

from requests import get

url = 'https://www.humblebundle.com/books'
html = get(url)
print(html.status_code)
name = 'humbleBundleWrequests.html'
obj_file = open('/home/dopel/codeInTest/humbleBundle/assetsNscript/assets/' + name, mode='w')
obj_file.write(html.text)
obj_file.close()
