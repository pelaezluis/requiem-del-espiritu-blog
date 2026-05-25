import os
from mysql import connector


class Connection:

    @classmethod
    def get_connection(cls):
        return connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=os.environ.get("DB_NAME", "blog"),
            port=int(os.environ.get("DB_PORT", 3306)),
        )
