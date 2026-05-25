from flask import session
from config import Connection


class DB:

    def __init__(self):
        self.db = Connection.get_connection()

    def close(self):
        if self.db and self.db.is_connected():
            self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def validate_login(self, username, password):
        cur = self.db.cursor()
        cur.execute(
            "select * from user where username = %s and password = %s",
            (username, password),
        )
        row = cur.fetchone()
        cur.close()
        return row

    def get_blogs(self):
        cur = self.db.cursor()
        if "username" in session:
            cur.execute(
                "select e.id, e.title, u.username, e.description, e.img, e.created_at, e.url "
                "from entrada e left join user u on u.id = e.user_id "
                "where u.username = %s",
                (session["username"],),
            )
        else:
            cur.execute(
                "select e.id, e.title, u.username, e.description, e.img, e.created_at, e.url "
                "from entrada e left join user u on u.id = e.user_id"
            )
        rows = cur.fetchall()
        cur.close()
        return rows

    def find_blog(self, ruta):
        cur = self.db.cursor()
        cur.execute(
            "select e.title, u.username, e.created_at, e.blog, e.description, e.img, e.url, e.song "
            "from entrada e left join user u on e.user_id = u.id "
            "where e.url = %s",
            (ruta,),
        )
        blog = cur.fetchone()
        cur.close()
        return blog

    def add_new_blog(self, data):
        cur = self.db.cursor()
        cur.execute(
            "insert into entrada(title, user_id, description, img, created_at, url, blog, song) "
            "values(%s, %s, %s, %s, NOW(), %s, %s, %s)",
            data,
        )
        self.db.commit()
        cur.close()

    def get_blog(self, id):
        cur = self.db.cursor()
        cur.execute("select * from entrada where id = %s", (id,))
        row = cur.fetchone()
        cur.close()
        return row

    def edit_blog(self, data):
        cur = self.db.cursor()
        cur.execute(
            "update entrada set title=%s, description=%s, img=%s, url=%s, blog=%s, song=%s "
            "where id=%s",
            data,
        )
        self.db.commit()
        cur.close()

    def delete_blog(self, id):
        cur = self.db.cursor()
        cur.execute("delete from entrada where id=%s", (id,))
        self.db.commit()
        cur.close()
