import os
from dotenv import load_dotenv
from flask import Flask, flash, render_template, redirect, session, request, url_for
from werkzeug.utils import secure_filename
from db import DB

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "qwerty")

path = "static/songs"
os.makedirs(path, exist_ok=True)
app.config["songs"] = path


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("auth/Login.html")

    username = request.form["username"]
    password = request.form["password"]
    try:
        db = DB()
        data = db.validate_login(username, password)
        db.close()
        if data is not None:
            session["user_id"] = data[0]
            session["username"] = data[2]
            return redirect("/poemas")
        else:
            flash("Usuario y/o contraseña erronea")
            return redirect("/login")
    except Exception as e:
        print(e)
        flash("Error de conexión con la base de datos")
        return redirect("/login")


@app.route("/", methods=["GET"])
def landing():
    return render_template("Landing.html", title="Requiem del espíritu | Inicio")


@app.route("/poemas", methods=["GET"])
def home():
    try:
        db = DB()
        blogs = db.get_blogs()
        db.close()
        return render_template(
            "Home.html", title="Requiem del espíritu | Poemas", blogs=blogs
        )
    except Exception as e:
        print(e)
        flash("Error al cargar los blogs")
        return redirect("/login")


@app.route("/blog/<string:ruta>")
def blog(ruta):
    try:
        db = DB()
        blog_data = db.find_blog(ruta)
        db.close()
        if blog_data is None:
            flash("Blog no encontrado")
            return redirect("/poemas")
        return render_template(
            "Blog.html", blog=blog_data, title=blog_data[0]
        )
    except Exception as e:
        print(e)
        flash("Error al cargar el blog")
        return redirect("/poemas")


@app.route("/blog/nuevo-blog", methods=["GET", "POST"])
def new_blog():
    if "username" not in session:
        return redirect("/")

    if request.method == "POST":
        try:
            db = DB()
            title = request.form["title"]
            autor = session["user_id"]
            description = request.form["description"]
            img = request.form["img"]
            url = request.form["url"]
            blog_content = request.form["blog"]
            song = request.files["song"]
            song_name = secure_filename(song.filename)
            song.save(os.path.join(path, song_name))
            data = (title, autor, description, img, url, blog_content, song_name)
            db.add_new_blog(data)
            db.close()
            return redirect("/poemas")
        except Exception as e:
            print(e)
            flash("Error al crear el blog")

    return render_template("NewBlog.html")


@app.route("/blog/<string:ruta>/editar/<id>", methods=["GET", "POST"])
def edit_blog(ruta, id):
    if "username" not in session:
        return redirect("/")
    try:
        db = DB()
        if request.method == "GET":
            blog_data = db.get_blog(id)
            db.close()
            if blog_data is None:
                flash("Blog no encontrado")
                return redirect("/poemas")
            return render_template("EditBlog.html", blog=blog_data)

        title = request.form["title"]
        description = request.form["description"]
        img = request.form["img"]
        url = request.form["url"]
        blog_content = request.form["blog"]
        song = request.files["song"]
        if song and song.filename:
            song_name = secure_filename(song.filename)
            song.save(os.path.join(path, song_name))
        else:
            song_name = request.form.get("current_song", "")
        data = (title, description, img, url, blog_content, song_name, id)
        db.edit_blog(data)
        db.close()
        return redirect("/poemas")
    except Exception as e:
        print(e)
        flash("Error al editar el blog")
        return redirect("/poemas")


@app.route("/blog/<string:ruta>/eliminar/<id>", methods=["GET", "POST"])
def delete_blog(ruta, id):
    if "username" not in session:
        return redirect("/")
    try:
        db = DB()
        db.delete_blog(id)
        db.close()
    except Exception as e:
        print(e)
        flash("Error al eliminar el blog")
    return redirect("/poemas")


@app.route("/deploy", methods=["POST"])
def deploy():
    token = request.headers.get("X-Deploy-Token")
    if token != os.environ.get("DEPLOY_SECRET"):
        return "Unauthorized", 401

    import subprocess

    repo_path = os.environ.get("REPO_PATH", os.getcwd())
    wsgi_path = os.environ.get("WSGI_PATH")

    if not wsgi_path:
        return "WSGI_PATH not configured", 500

    try:
        subprocess.run(["git", "pull"], cwd=repo_path, capture_output=True, text=True, check=True)
        subprocess.run(["touch", wsgi_path], capture_output=True, check=True)
        return "Deployed", 200
    except subprocess.CalledProcessError as e:
        return f"Deploy failed: {e.stderr}", 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 3000)),
        debug=True,
    )
