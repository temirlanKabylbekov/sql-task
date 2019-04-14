from contextlib import closing

import pytest

import settings
from conftest import STRESS_TEST_REPEAT_COUNT, Factory
from main import get_result


@pytest.mark.repeat(STRESS_TEST_REPEAT_COUNT)
def test_initial(db_migrations, db_data, benchmark):
    db_conn = db_migrations(settings.MIGRATION_INITIAL)
    with closing(db_conn) as conn:
        db_data(conn, 'exchange_rates', Factory.exchange_rates(10))
        assert benchmark(get_result, conn) == 2
