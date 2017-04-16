import rethinkdb as r


def get_connection(db_name=None):
    options = {
        'host': 'localhost',
        'port': 9901
    }

    if db_name:
        options.update({'db': db_name})

    return r.connect(**options)
