
from flask import session
from config import Connection

class DB:

    def __init__(self):
        self.db = Connection.dev_connection()


    def validate_login(self, username, password):
        """
        Validar si un usuario existe
        """
        cur = self.db.cursor()
        sql = "select * from user where username = %s and password = %s"
        cur.execute(sql, (username, password))
        row = cur.fetchone()
        if row:
            return row
        else:
            print('Usuario y/o contraseña inválida')


    def get_blogs(self):
        """
            Obtener todos los blogs
        """
        if 'username' in session:
            sql = "select e.id, e.title, u.username,e.description, e.img, e.created_at, e.url from entrada e left join user u on u.id = e.user_id having u.username =%s;"
            cur = self.db.cursor()
            cur.execute(sql, (session['username'],))
            blogs = cur.fetchall()
            return blogs
        else:
            sql = "select e.id, e.title, u.username,e.description, e.img, e.created_at, e.url from entrada e left join user u on u.id = e.user_id;"
            cur = self.db.cursor()
            cur.execute(sql)
            blogs = cur.fetchall()
            return blogs

    def find_blog(self, ruta):
        """
            Obtener blog por ruta
        """
        sql = "select e.title, u.username, e.created_at, e.blog, e.description, e.img, e.url, e.song from entrada e left join user u on e.user_id=u.id having e.url =%s;"
        cur = self.db.cursor()
        cur.execute(sql, (ruta,))
        blog = cur.fetchone()
        return blog

    def add_new_blog(self, data):
        """
            Inserta una nueva entrada en la db
        """
        sql = "insert into entrada(title, user_id, description, img, created_at, url, blog, song) values(%s, %s, %s, %s, NOW(), %s, %s, %s)"
        cur = self.db.cursor()
        cur.execute(sql, data)
        self.db.commit()

    
    def get_blog(self, id):
        """
            Extrae una entrada existente
        """
        sql = "select * from entrada where id = %s"
        cur = self.db.cursor()
        cur.execute(sql, (id,))
        row = cur.fetchone()
        print(row)
        if len(row) > 0:
            return row
        else:
            print('Entrada no existe')


    def edit_blog(self, data):
        """
            Modifica una entrada
        """
        sql = "UPDATE entrada set title=%s, description=%s, img=%s, url=%s, blog=%s, song=%s WHERE id=%s"
        cur = self.db.cursor()
        cur.execute(sql, data)
        self.db.commit()


    def delete_blog(self, id):
        sql = "delete from entrada where id=%s"
        cur = self.db.cursor()
        cur.execute(sql, (id,))
        self.db.commit()