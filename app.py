from flask import Flask, flash, render_template, redirect, session, url_for, request
from db import DB


app = Flask(__name__)
app.secret_key = "qwerty"


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'GET':
        return render_template('auth/Login.html')

    elif request.method == 'POST':
        db = DB()
        username = request.form['username']
        password = request.form['password'] 
        data = db.validate_login(username, password)
        # print(data)
        if data != None:
            print('Iniciando sesión')
            session['user_id'] = data[0]
            session['username'] = data[2]
            return redirect('/')
        else:
            return redirect('/login')


@app.route('/', methods=['GET'])
def home():
    """
        Obtener todos los blogs
    """
    db = DB()
    blogs = db.get_blogs()
    # print(blogs)
    return render_template('Home.html', title="Requiem del espíritu | Inicio", blogs=blogs)


@app.route('/blog/<string:ruta>')
def blog(ruta):
    db = DB()
    blog = db.find_blog(ruta)
    # print(blog)
    return render_template("Blog.html", blog=blog, title=blog[0])


@app.route('/blog/nuevo-blog', methods=['GET', 'POST'])
def new_blog():
    """
        Se crea una nueva entrada
    """
    if 'username' not in session:
        return redirect('/')

    if request.method == 'POST':
        db = DB()
        title = request.form['title']
        autor = session['user_id']
        description = request.form['description']
        img = request.form['img']
        url = request.form['url']
        blog = request.form['blog']
        data = (title, autor, description, img, url, blog)
        db.add_new_blog(data)
        return redirect('/')
        
    elif request.method == 'GET':
        return render_template('NewBlog.html')


@app.route('/blog/<string:ruta>/editar/<id>', methods=['GET', 'POST'])
def edit_blog(ruta, id):
    db = DB()
    if request.method == 'GET':
        blog = db.get_blog(id)
        return render_template('EditBlog.html', blog=blog)
        
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        img = request.form['img']
        url = request.form['url']
        blog = request.form['blog']
        data = (title, description, img, url, blog, id)
        db.edit_blog(data)
        return redirect('/')
    


@app.route('/blog/<string:ruta>/eliminar/<id>', methods=['GET', 'POST'])
def delete_blog(ruta, id):
    if 'username' in session:
        db = DB()
        db.delete_blog(id)
        return redirect('/')

if __name__ == "__main__":
    app.run(
        port=3000,
        debug=True
    )