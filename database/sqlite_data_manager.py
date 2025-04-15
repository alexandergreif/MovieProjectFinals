from .datamanager_interface import DataManagerInterface
from .models import db, User, Movie

class SQLiteDataManager(DataManagerInterface):
    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        user = User.query.get(user_id)
        return user.movies if user else []

    def add_user(self, name):
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def add_movie(self, user_id, title, year, rating, poster):
        movie = Movie(title=title, year=year, rating=rating, poster=poster, user_id=user_id)
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, title, year, rating, poster):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = title
            movie.year = year
            movie.rating = rating
            movie.poster = poster
            db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie

    def search_movies(self, query="", sort_by="title"):
        query = query.strip().lower()
        movies = Movie.query

        if query:
            movies = movies.filter(Movie.title.ilike(f"%{query}%"))

        if sort_by == "year":
            movies = movies.order_by(Movie.year.desc())
        elif sort_by == "rating":
            movies = movies.order_by(Movie.rating.desc())
        else:
            movies = movies.order_by(Movie.title.asc())

        return movies.all()


    def get_all_movies(self, query=None, sort_by=None):
        movies_query = Movie.query

        if query:
            movies_query = movies_query.filter(Movie.title.ilike(f"%{query}%"))

        if sort_by == "title":
            movies_query = movies_query.order_by(Movie.title.asc())
        elif sort_by == "year":
            movies_query = movies_query.order_by(Movie.year.desc())
        elif sort_by == "rating":
            movies_query = movies_query.order_by(Movie.rating.desc())

        return movies_query.all()

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False