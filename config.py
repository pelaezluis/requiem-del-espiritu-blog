import os
import pymysql


class Connection:

    @classmethod
    def get_connection(cls):
        host = os.environ.get("DB_HOST", "localhost")
        user = os.environ.get("DB_USER", "root")
        password = os.environ.get("DB_PASSWORD", "")
        database = os.environ.get("DB_NAME", "blog")
        port = int(os.environ.get("DB_PORT", 3306))

        print(f"[DB CONFIG] host={host} user={user} db={database} port={port}")
        print(f"[DB CONFIG] password_len={len(password)}")

        return pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            charset="utf8mb4",
        )
