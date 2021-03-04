#!/usr/bin/bash

assets_path="/home/dopel/codeInTest/humbleBundle/assetsNscript/assets"
list=$(ls $assets_path)
echo 'se borrara el archivo '$list
rm $assets_path'/'$list
echo "se borro el arch¡vo $list de la carperta $assets_path"
