import datetime
import random
from contextlib import closing

import psycopg2
import pytest
from faker import Faker
from psycopg2 import sql

import settings

STRESS_TEST_REPEAT_COUNT = 5


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


class Factory:
    @classmethod
    def faker(cls):
        return Faker()

    @classmethod
    def exchange_rate(cls):
        currencies = ['USD', 'GBP', 'EUR', 'HUF', 'RUB']
        start_datetime = datetime.datetime(2018, 4, 1)
        end_datetime = datetime.datetime(2018, 4, 2)
        start_rate = 0.01
        end_rate = 1.99
        rate_digits = 3

        ts = cls.faker().date_time_between_dates(datetime_start=start_datetime, datetime_end=end_datetime, tzinfo=None)
        from_currency = random.choice(currencies)
        to_currency = random.choice(list(set(currencies) - set([from_currency])))
        rate = round(random.uniform(start_rate, end_rate), rate_digits)
        return (str(ts), from_currency, to_currency, rate)

    @classmethod
    def transaction(cls, users_count):
        currencies = ['USD', 'GBP', 'EUR', 'HUF', 'RUB']
        start_datetime = datetime.datetime(2018, 4, 1)
        end_datetime = datetime.datetime(2018, 4, 2)
        start_amount = 0.1
        end_amount = 99.99
        amount_digits = 2

        ts = cls.faker().date_time_between_dates(datetime_start=start_datetime, datetime_end=end_datetime, tzinfo=None).replace(second=0)
        user_id = random.randint(1, users_count)
        currency = random.choice(currencies)
        amount = round(random.uniform(start_amount, end_amount), amount_digits)
        return (str(ts), user_id, currency, amount)

    @classmethod
    def exchange_rates(cls, count):
        for _ in range(count):
            yield cls.exchange_rate()

    @classmethod
    def transactions(cls, count, users_count):
        for _ in range(count):
            yield Factory.transaction(users_count)
