from contextlib import closing

import settings


class TestInitial:
    def test_initial(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_INITIAL)
        with closing(db_conn) as conn:
            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:00:00', 'USD', 'GBP', 0.71),
                ('2018-04-01 00:00:05', 'USD', 'GBP', 0.82),
            ])


def test_with_indexes():
    pass


def test_with_new_schema():
    pass


def test_with_sharding():
    pass
