from typing import NamedTuple

class Settings(NamedTuple):
    pguser: str
    pgpassword: str
    pgdatabase: str
    pghost: str
    pgport: str

def get_settings():
    settings = Settings(
        pguser = 'postgres',
        pgpassword = 'postgres',
        pgdatabase = 'test',
        pghost = '192.168.18.58',
        pgport = '5432',
    )
    return settings

