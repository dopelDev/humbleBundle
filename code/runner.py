from json_data_downloader import load_data, remove_tag, save_json, load_decode_json, download_html, cleanAssets, print_categories
from sys import executable

print(executable)
path = '/home/dopel/codeInTest/humbleBundle'
download_html(path)
save_json(remove_tag(load_data(path)), path)
json_file = load_decode_json(path)
print(print_categories(json_file))
cleanAssets(path)
