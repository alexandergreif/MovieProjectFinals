import os
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
from database.models import User, Movie
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set in .env!")

#api_key = os.getenv("OMDB_API_KEY") #used for importing data via api from IMDB

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database", "movies.sqlite3")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/explore")
def explore_movies():
    query = request.args.get("q", "").strip().lower()

    if query:
        movies = Movie.query.filter(Movie.title.ilike(f"%{query}%")).all()
    else:
        movies = Movie.query.all()

    return render_template("explore.html", movies=movies, search_query=query)

@app.route("/users/<int:user_id>", methods=['GET','POST'])
def add_movie(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        title = request.form["title"]
        year = int(request.form["year"])
        rating = float(request.form["rating"])
        poster = request.form["poster"]

        movie = Movie(title=title, year=year, rating=rating, poster=poster, user_id=user.id)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for("user_movies", user_id=user.id))

    return render_template("add_movie.html", user=user)

@app.route("/update/<movie_id>", methods=['GET', 'POST'])
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        movie.title = request.form["title"]
        movie.year = int(request.form["year"])
        movie.rating = float(request.form["rating"])
        movie.poster = request.form["poster"]

        db.session.commit()
        return redirect(url_for("explore_movies"))
    return render_template("update_movie.html", movie=movie)

@app.route("/delete/<movie_id>")
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash(f"'{movie.title}' was deleted successfully!", "success")
    return redirect(url_for("explore_movies"))

@app.route("/users", methods=['GET'])
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/int:<user_id>")
def user_movies(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("explore.html", movies=user.movies, user=user)

@app.route("/add_user", methods=['GET', 'POST'])
def add_user():

    if request.method == 'POST':
        name = request.form["name"]
        if name.strip():
            new_user = User(name=name.strip())
            db.session.add(new_user)
            db.session.commit()
            flash(f"User '{new_user.name}' created successfully!", "success")
            return redirect(url_for("user_movies", user_id=new_user.id))
        else:
            flash("Please enter a valid name.", "danger")
    return render_template("add_user.html")



if __name__ == "__main__":
    app.run(debug=True)