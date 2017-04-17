import rdbpy.db_objects as dbo

from rdbpy.conn import get_connection

if __name__ == '__main__':
    rdb_conn = get_connection('linux')
    fs_nodes = dbo.FSNodes(rdb_conn)
    result = fs_nodes.report_python()
    print(result)
