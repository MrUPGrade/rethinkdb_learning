import argparse
import logging
import sys
import magic
import time

from pathlib import Path

from rdbpy.conn import get_connection
import rdbpy.db_objects as dbo


def setup_logger():
    log_file = Path(__file__).parent / '..' / 'log'
    log_file = log_file.resolve() / ('disc_scan-%d.log' % time.time())
    logging.basicConfig(filename=str(log_file), level=logging.DEBUG)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Program for scanning your local file system')
    parser.add_argument('-p', '--path', dest='path')

    return parser.parse_args()


def get_search_path_from_args(args):
    if args.path:
        root = Path(args.path)
        try:
            root = root.resolve()
        except FileNotFoundError:
            print('Path: "%s" is not a correct path.' % root)
            sys.exit(-1)

        if not root.is_dir():
            print('Path: "%s" is not a correct path.' % root)
            sys.exit(-1)

    else:
        root = Path(__file__)

    return root


def walk_path(src_path, path_callback):
    if src_path.is_dir():
        for p in src_path.iterdir():
            yield from walk_path(p, path_callback=path_callback)
    else:
        yield path_callback(src_path)


def path_printer(path):
    result = {
        'path': str(path),
        'parent': str(path.parent),
    }

    try:
        file_stat = path.stat()
    except FileNotFoundError:
        if path.is_symlink():
            logging.debug('broken link: %s' % path)
            result.update({'status': 'broken'})
    else:
        result.update({
            'size': file_stat.st_size,
            'atime': file_stat.st_atime,
            'mtime': file_stat.st_mtime,
            'ctime': file_stat.st_ctime,
            'uid': file_stat.st_uid,
            'gid': file_stat.st_gid,
            'links': file_stat.st_nlink
        })

        file_type = magic.from_file(str(path))
        file_mime = magic.from_file(str(path), mime=True)

        result.update({
            'type': file_type,
            'mime': file_mime
        })

    return result


if __name__ == '__main__':
    setup_logger()
    args = parse_arguments()
    root_path = get_search_path_from_args(args)

    rdb_conn = get_connection()

    db = dbo.DB('linux', rdb_conn)
    db.create_database()

    rdb_conn.use('linux')

    table = dbo.RDBTable('fs_nodes', rdb_conn)
    table.create_table()

    fs_nodes = dbo.FSNodes(rdb_conn)

    for fs_node_data in walk_path(root_path, path_callback=path_printer):
        fs_nodes.add_node(fs_node_data)
