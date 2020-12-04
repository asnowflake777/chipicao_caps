DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 5000

DB_HOST = '127.0.0.1'
DB_PORT = 5432
DB_USER = 'chipicao'
DB_PASSWORD = 'password'
DATABASE = 'chipicao_db'

DB_URL = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}'
MODULES = {"models": ['models']}
