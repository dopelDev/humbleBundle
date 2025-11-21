#!/usr/bin/env python3
"""
Script para recrear la base de datos.
Elimina y recrea todas las tablas.
"""
from spider.database.persistence import recreate_database
from spider.config.settings import get_settings

if __name__ == '__main__':
    settings = get_settings()
    print(f'Recreando base de datos: {settings.pgdatabase}')
    recreate_database(settings, drop_existing=True)
    print('Base de datos recreada exitosamente')

