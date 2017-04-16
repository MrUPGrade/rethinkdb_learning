import rethinkdb as r


class DB:
    def __init__(self, db_name, connection):
        self._conn = connection
        self._name = db_name

    def create_database(self):
        r.db_create(self._name).run(self._conn)

    def drop_database(self):
        r.db_drop(self._name).run(self._conn)


    def ensure_created(self):
        res = r.db_list().run(self._conn)

        if self._name not in res:
            self.create_database()

    def ensure_dropped(self):
        res = r.db_list().run(self._conn)

        if self._name in res:
            self.drop_database()


class RDBTable:
    def __init__(self, table_name, connection):
        self._table_name = table_name
        self._conn = connection

    def create_table(self):
        r.table_create(self._table_name).run(self._conn)

    def drop_table(self):
        r.table_drop(self._table_name).run(self._conn)

    def ensure_created(self):
        res = r.table_list().run(self._conn)

        if self._table_name not in res:
            self.create_table()

    def ensure_dropped(self):
        res = r.table_list().run(self._conn)

        if self._table_name in res:
            self.drop_table()


class Files:
    def __init__(self, connection):
        self._conn = connection
