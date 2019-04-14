import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

CURRENT_DIR = os.getcwd()

MIGRATIONS_FOLDER = 'migrations'
MIGRATION_INITIAL = os.path.join(CURRENT_DIR, MIGRATIONS_FOLDER, 'initial.sql')
