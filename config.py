import locale

DEBUG = True

DATABASE = {
    "provider": 'mysql',
    "host": 'localhost',
    "user": 'mp_zspo',
    "passwd": 'Vjkgfhk2020@',
    "database": 'mp_zspo',
}
"""
Variation DATABASE
    provider='sqlite', filename=':memory:'
    provider='sqlite', filename='filename', create_db=True
    provider='mysql', host='', user='', passwd='', db=''
    provider='oracle', user='', password='', dsn=''
    provider='cockroach', user='', password='', host='', database='', sslmode='disable'
"""

MIGRATION_DIR = 'migration'

RESOURCE_CACHE = 60 * 60 * 24 * 7  # 1 week


try:
    locale.setlocale(locale.LC_TIME, "ru_RU")
    DATE_FORMAT = "%d %b %Y"

except BaseException as err:
    print("I18n error! %s: %s" % (type(err).__name__, err))
    DATE_FORMAT = "%d.%m.%Y"
