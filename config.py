import os
import MySQLdb


class Connection:

    @classmethod
    def get_connection(cls):
        host = os.environ.get("DB_HOST", "localhost")
        user = os.environ.get("DB_USER", "root")
        password = os.environ.get("DB_PASSWORD", "")
        database = os.environ.get("DB_NAME", "blog")
        port = int(os.environ.get("DB_PORT", 3306))

        return MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=database,
            port=port,
            charset="utf8mb4",
        )
