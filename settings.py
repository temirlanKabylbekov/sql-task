import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

CURRENT_DIR = os.getcwd()

MIGRATIONS_FOLDER = 'migrations'
MIGRATION_INITIAL = os.path.join(CURRENT_DIR, MIGRATIONS_FOLDER, '1-initial.sql')
MIGRATION_WITH_NEW_SCHEMA = os.path.join(CURRENT_DIR, MIGRATIONS_FOLDER, '2-with_new_schema.sql')
MIGRATION_WITH_INDEXES = os.path.join(CURRENT_DIR, MIGRATIONS_FOLDER, '3-with_indexes.sql')
