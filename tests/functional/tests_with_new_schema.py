from contextlib import closing

import settings
from main import get_result_for_new_schema, round_number_to_decimal


class TestWithNewSchema:
    def test_initial_data(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:00:00', 'USD', 'GBP', '0.71'),
                ('2018-04-01 00:00:05', 'USD', 'GBP', '0.82'),
                ('2018-04-01 00:01:00', 'USD', 'GBP', '0.92'),
                ('2018-04-01 01:02:00', 'USD', 'GBP', '0.62'),

                ('2018-04-01 02:00:00', 'USD', 'GBP', '0.71'),
                ('2018-04-01 03:00:05', 'USD', 'GBP', '0.82'),
                ('2018-04-01 04:01:00', 'USD', 'GBP', '0.92'),
                ('2018-04-01 04:22:00', 'USD', 'GBP', '0.62'),

                ('2018-04-01 00:00:00', 'EUR', 'GBP', '1.71'),
                ('2018-04-01 01:00:05', 'EUR', 'GBP', '1.82'),
                ('2018-04-01 01:01:00', 'EUR', 'GBP', '1.92'),
                ('2018-04-01 01:02:00', 'EUR', 'GBP', '1.62'),

                ('2018-04-01 02:00:00', 'EUR', 'GBP', '1.71'),
                ('2018-04-01 03:00:05', 'EUR', 'GBP', '1.82'),
                ('2018-04-01 04:01:00', 'EUR', 'GBP', '1.92'),
                ('2018-04-01 05:22:00', 'EUR', 'GBP', '1.62'),

                ('2018-04-01 05:22:00', 'EUR', 'HUF', '0.062'),
            ])

            db_data(conn, 'transactions', [
                ('2018-04-01 00:00:00', 1, 'EUR', 2.45),
                ('2018-04-01 01:00:00', 1, 'EUR', 8.45),
                ('2018-04-01 01:30:00', 1, 'USD', 3.5),
                ('2018-04-01 20:00:00', 1, 'EUR', 2.45),

                ('2018-04-01 00:30:00', 2, 'USD', 2.45),
                ('2018-04-01 01:20:00', 2, 'USD', 0.45),
                ('2018-04-01 01:40:00', 2, 'USD', 33.5),
                ('2018-04-01 18:00:00', 2, 'EUR', 12.45),

                ('2018-04-01 18:01:00', 3, 'GBP', 2),

                ('2018-04-01 00:01:00', 4, 'USD', 2),
                ('2018-04-01 00:01:00', 4, 'GBP', 2),
            ])

            expected = [
                (1, round_number_to_decimal(2.45 * 1.71 + 8.45 * 1.71 + 3.5 * 0.62 + 2.45 * 1.62, 3)),
                (2, round_number_to_decimal(2.45 * 0.92 + 0.45 * 0.62 + 33.5 * 0.62 + 12.45 * 1.62, 3)),
                (3, round_number_to_decimal(2 * 1, 3)),
                (4, round_number_to_decimal(2 * 0.92 + 2 * 1, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_empty_transactions(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:00:00', 'USD', 'GBP', '0.71'),
                ('2018-04-01 01:02:00', 'EUR', 'GBP', '1.62'),
                ('2018-04-01 05:22:00', 'EUR', 'HUF', '0.062'),
            ])
            assert get_result_for_new_schema(conn, 'GBP') == []

    def test_empty_exchange_rates_and_transaction_with_target_currenc(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
            ])

            db_data(conn, 'transactions', [
                ('2018-04-01 00:00:00', 1, 'EUR', 2.45),
                ('2018-04-01 00:30:00', 2, 'USD', 2.45),
                ('2018-04-01 01:20:00', 2, 'USD', 0.45),
                ('2018-04-01 18:01:00', 3, 'GBP', 2),
            ])
            expected = [
                (3, round_number_to_decimal(2 * 1, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_empty_transactions_and_exchange_rates(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])
            assert get_result_for_new_schema(conn, 'GBP') == []

    def test_exchange_rates_to_gbp_are_absent(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:00:00', 'USD', 'EUR', '0.71'),
                ('2018-04-01 01:02:00', 'EUR', 'HUF', '1.62'),
                ('2018-04-01 05:22:00', 'EUR', 'HUF', '0.062'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:00:00', 1, 'EUR', 2.45),
                ('2018-04-01 00:30:00', 2, 'USD', 2.45),
                ('2018-04-01 01:20:00', 2, 'USD', 0.45),
                ('2018-04-01 18:01:00', 3, 'GBP', 2),
            ])
            expected = [
                (3, round_number_to_decimal(2 * 1, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_exchange_rates_for_given_transactions_are_absent(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 23:00:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 2, 'USD', 2.45),
            ])
            assert get_result_for_new_schema(conn, 'GBP') == []

    def test_transactions_without_currency(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 2, None, 2.45),
            ])
            assert get_result_for_new_schema(conn, 'GBP') == []

    def test_transactions_without_amount(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 2, 'USD', None),
            ])
            expected = [
                (2, round_number_to_decimal(0, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_transactions_without_amount_not_including_in_result(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 2, 'USD', None),
                ('2018-04-01 00:40:00', 2, 'USD', '2'),
            ])
            expected = [
                (2, round_number_to_decimal(2 * 1.5, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_transactions_without_user_id(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', None, 'USD', '2'),
                ('2018-04-01 00:32:00', None, 'USD', '3'),
                ('2018-04-01 00:30:00', 3, 'USD', '3'),
            ])
            expected = [
                (3, round_number_to_decimal(3 * 1.5, 3)),
                (None, round_number_to_decimal((3 + 2) * 1.5, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_transactions_without_timestamp(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                (None, 2, 'USD', '2'),
            ])
            assert get_result_for_new_schema(conn, 'GBP') == []

    def test_sorting_by_user_id(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 3, 'USD', '2'),
                ('2018-04-01 00:35:00', 1, 'USD', '3'),
                ('2018-04-01 00:45:00', 2, 'GBP', '3'),
            ])
            expected = [
                (1, round_number_to_decimal(3 * 1.5, 3)),
                (2, round_number_to_decimal(3 * 1, 3)),
                (3, round_number_to_decimal(2 * 1.5, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_transactions_to_gbp_without_amount(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 3, 'GBP', None),
            ])
            expected = [
                (3, round_number_to_decimal(0, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_transactions_only_to_gbp(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 3, 'GBP', '2'),
                ('2018-04-01 00:35:00', 3, 'GBP', '3'),
                ('2018-04-01 00:45:00', 2, 'GBP', '4'),
            ])
            expected = [
                (2, round_number_to_decimal(4 * 1, 3)),
                (3, round_number_to_decimal((2 + 3) * 1, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_transactions_not_contain_to_gbp_transactions(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:21:00', 'EUR', 'GBP', '2.5'),
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 3, 'USD', '2'),
                ('2018-04-01 00:35:00', 2, 'EUR', '3'),
            ])
            expected = [
                (2, round_number_to_decimal(3 * 2.5, 3)),
                (3, round_number_to_decimal(2 * 1.5, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_use_equal_exchange_rate_timestamp(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:19:59', 'USD', 'GBP', '2.5'),
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:20:00', 3, 'USD', '2'),
            ])
            expected = [
                (3, round_number_to_decimal(2 * 1.5, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected

    def test_several_exchange_rates_with_the_same_timestamp(self, db_migrations, db_data):
        db_conn = db_migrations(settings.MIGRATION_WITH_NEW_SCHEMA)
        with closing(db_conn) as conn:
            # preliminary data migration
            db_data(conn, 'exchange_rates', [
                ('1970-01-01 00:00:00', 'USD', 'USD', '1'),
                ('1970-01-01 00:00:00', 'GBP', 'GBP', '1'),
                ('1970-01-01 00:00:00', 'EUR', 'EUR', '1'),
                ('1970-01-01 00:00:00', 'HUF', 'HUF', '1'),
            ])

            db_data(conn, 'exchange_rates', [
                ('2018-04-01 00:20:00', 'USD', 'GBP', '1.5'),
                ('2018-04-01 00:20:00', 'EUR', 'GBP', '2.5'),
            ])
            db_data(conn, 'transactions', [
                ('2018-04-01 00:30:00', 3, 'USD', '2'),
                ('2018-04-01 00:35:00', 2, 'EUR', '3'),
            ])
            expected = [
                (2, round_number_to_decimal(3 * 2.5, 3)),
                (3, round_number_to_decimal(2 * 1.5, 3)),
            ]
            assert get_result_for_new_schema(conn, 'GBP') == expected
