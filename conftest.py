from contextlib import closing

import psycopg2
import pytest
from psycopg2 import sql

import settings


def get_db_conn(db_name):
    conn = psycopg2.connect(dbname=db_name, user=settings.DB_USER,
                            password=settings.DB_PASSWORD, host=settings.DB_HOST)
    conn.autocommit = True
    return conn


@pytest.fixture
def db_database(faker):
    """creates new database and returns connection to it"""
    def _db_database():
        db_name = faker.slug()
        with closing(get_db_conn('postgres')) as conn:
            with conn.cursor() as cursor:
                create_database = sql.SQL(f'CREATE DATABASE "{db_name}";')
                cursor.execute(create_database)
        return get_db_conn(db_name)
    return _db_database


@pytest.fixture
def db_migrations(db_database):
    """runs migration from file on created new database and returns connection to it"""
    def _db_migrations(migration_path):
        conn = db_database()
        with conn.cursor() as cursor:
            cursor.execute(open(migration_path, 'r').read())
        return conn
    return _db_migrations


@pytest.fixture
def db_data():
    """loads data(list of tuples) in given table"""
    def _db_data(conn, table, data):
        with conn.cursor() as cursor:
            insert_data = sql.SQL(',').join(map(sql.Literal, data)).as_string(cursor)
            insert_data = sql.SQL(f'INSERT INTO {table} VALUES {insert_data};')
            cursor.execute(insert_data)
    return _db_data
