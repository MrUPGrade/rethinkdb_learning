import rethinkdb as r
from rdbpy.db_objects import RDBTable


def test_ensure_created(db_test_conn):
    table = RDBTable(table_name='ensure_created_test1', connection=db_test_conn)
    table.ensure_created()

    assert 'ensure_created_test1' in r.table_list().run(db_test_conn)


def test_ensure_created_can_run_multiple_times(db_test_conn):
    table = RDBTable(table_name='ensure_created_test2', connection=db_test_conn)
    table.ensure_created()
    table.ensure_created()

    assert 'ensure_created_test2' in r.table_list().run(db_test_conn)


def test_ensure_dropped(db_test_conn):
    table = RDBTable(table_name='ensure_drop_test1', connection=db_test_conn)
    table.ensure_dropped()

    assert 'ensure_drop_test1' not in r.table_list().run(db_test_conn)


def test_ensure_dropped_can_run_multiple_times(db_test_conn):
    table = RDBTable(table_name='ensure_drop_test2', connection=db_test_conn)
    table.ensure_dropped()
    table.ensure_dropped()

    assert 'ensure_drop_test2' not in r.table_list().run(db_test_conn)
