import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from database import db
from database.models import User, Movie
from dotenv import load_dotenv
from database.sqlite_data_manager import SQLiteDataManager

data_manager = SQLiteDataManager()

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
    try:
        return render_template("index.html")
    except Exception as e:
        app.logger.error(f"Home page failed: {e}")
        flash("Something went wrong loading the home page.", "danger")
        return redirect(url_for("list_users"))

@app.route("/explore")
def explore_movies():
    try:
        query = request.args.get("q", "").strip().lower()
        user_id = request.args.get("user_id")

        user = User.query.get(user_id) if user_id else None
        movies = data_manager.search_movies(query)
        favorite_movies = [m for m in movies if user and m.favorite and m.user_id == user.id]

        return render_template("explore.html", movies=movies, favorite_movies=favorite_movies, search_query=query, user=user)
    except Exception as e:
        app.logger.error(f"Search error: {e}")
        flash("Something went wrong with your search. Try again.", "danger")
        return render_template("explore.html", movies=[], search_query="", favorite_movies=[], user=None)

@app.route("/users/<int:user_id>/add_movie", methods=['GET', 'POST'])
def add_movie(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        try:
            title = request.form["title"]
            year = int(request.form["year"])
            rating = float(request.form["rating"])
            poster = request.form["poster"]

            if not title:
                flash("Title is required.", "danger")
            elif year < 1888 or year > 2100:
                flash("Please enter a valid release year (1888–2100).", "danger")
            elif rating < 0 or rating > 10:
                flash("Rating must be between 0 and 10.", "danger")
            elif not poster.startswith("http"):
                flash("Please enter a valid poster URL.", "danger")
            else:
                data_manager.add_movie(user_id, title, year, rating, poster)
                flash("Movie added successfully!", "success")
                return redirect(url_for("explore_movies", user_id=user.id))

        except ValueError:
            flash("Year must be a number and rating must be a valid float.", "danger")
        except Exception as e:
            app.logger.error(f"Add movie failed: {e}")
            flash("Something went wrong while adding the movie.", "danger")

    return render_template("add_movie.html", user=user)

@app.route("/update/<movie_id>", methods=['GET', 'POST'])
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        try:
            title = request.form["title"]
            year = int(request.form["year"])
            rating = float(request.form["rating"])
            poster = request.form["poster"]

            # Validation logic
            if not title:
                flash("Title is required.", "danger")
            elif year < 1888 or year > 2100:
                flash("Please enter a valid release year (1888–2100).", "danger")
            elif rating < 0 or rating > 10:
                flash("Rating must be between 0 and 10.", "danger")
            elif not poster.startswith("http"):
                flash("Please enter a valid poster URL.", "danger")
            else:
                data_manager.update_movie(movie_id, title, year, rating, poster)
                flash("Movie updated successfully!", "success")
                return redirect(url_for("explore_movies", user_id=movie.user_id))

        except ValueError:
            flash("Year must be a number and rating must be a valid float.", "danger")
        except Exception as e:
            app.logger.error(f"Error updating movie {movie_id}: {e}")
            flash("Failed to update the movie. Please try again.", "danger")

    return render_template("update_movie.html", movie=movie)

@app.route("/delete/<movie_id>")
def delete_movie(movie_id):
    try:
        movie = Movie.query.get_or_404(movie_id)
        data_manager.delete_movie(movie_id)
        flash(f"'{movie.title}' was deleted successfully!", "success")
    except Exception as e:
        app.logger.error(f"Error deleting movie {movie_id}: {e}")
        flash("Could not delete the movie. Please try again.", "danger")

    return redirect(url_for("explore_movies"))

@app.route("/users")
def list_users():
    try:
        users = User.query.filter_by(is_active=True).all()
        return render_template("users.html", users=users)
    except Exception as e:
        app.logger.error(f"Error loading users: {e}")
        flash("Failed to load users.", "danger")
        return render_template("users.html", users=[])


@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form["name"].strip()
        if name:
            try:
                new_user = data_manager.add_user(name)
                flash(f"User '{new_user.name}' created successfully!", "success")
                return redirect(url_for("explore_movies", user_id=new_user.id))
            except IntegrityError:
                db.session.rollback()  # important to reset the failed transaction
                flash("That username is already taken. Please choose another.", "danger")
            except Exception as e:
                app.logger.error(f"Unexpected error while adding user: {e}")
                flash("An unexpected error occurred. Please try again.", "danger")
        else:
            flash("Please enter a valid name.", "danger")
    return render_template("add_user.html")


@app.route("/favorite/<int:movie_id>", methods=['POST'])
def toggle_favorite(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    movie.favorite = not movie.favorite
    db.session.commit()
    flash(f"{'Added to' if movie.favorite else 'Removed from'} favorites!", "info")
    return redirect(url_for("explore_movies", user_id=movie.user_id))

@app.route("/choose_user")
def choose_user():
    next_page = request.args.get("next", "explore")  # either 'explore' or 'add'
    users = User.query.filter_by(is_active=True).all()
    return render_template("choose_user.html", users=users, next_page=next_page)

@app.route("/users/<int:user_id>/deactivate", methods=["POST"])
def deactivate_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user.is_active = False
        db.session.commit()
        flash(f"User '{user.name}' has been deactivated.", "info")
    except Exception as e:
        app.logger.error(f"Failed to deactivate user {user_id}: {e}")
        flash("Something went wrong while deactivating the user.", "danger")

    return redirect(url_for("list_users"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500



if __name__ == "__main__":
    app.run(debug=True)