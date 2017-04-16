import pytest

import rethinkdb as r

from rdbpy.conn import get_connection


@pytest.fixture(scope='module')
def db_test_conn(request):
    conn = get_connection()

    r.db_create('e2e_tests').run(conn)
    conn.use('e2e_tests')

    def fin():
        r.db_drop('e2e_tests').run(conn)
        conn.close()

    request.addfinalizer(fin)

    return conn


@pytest.fixture(scope='module')
def srv_conn(request):
    conn = get_connection()

    def fin():
        conn.close()

    request.addfinalizer(fin)

    return conn
