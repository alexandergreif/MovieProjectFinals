from .datamanager_interface import DataManagerInterface
from .models import db, User, Movie, Favorite


class SQLiteDataManager(DataManagerInterface):
    def get_all_users(self):
        """
        Return every user in the system.

        Returns:
            list[User]: List of user objects (maybe empty).
        """
        return User.query.all()

    def get_user_movies(self, user_id):
        """
        Return all movies that belong to a user.

        Args:
            user_id (int): User primary key.

        Returns:
            list[Movie]: The user's movie list, or an empty list if
            the user does not exist.
        """
        user = User.query.get(user_id)
        return user.movies if user else []

    def add_user(self, name):
        """
        Create and persist a new user.

        Args:
            name (str): Display name (must be unique).

        Returns:
            User: The newly created user instance.
        """
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def add_movie(self, user_id, title, year, rating, poster):
        """
        Insert a new movie record.

        Args:
            user_id (int): Owner of the movie.
            title (str): Movie title.
            year (int): Release year.
            rating (float): Rating on a 0–10 scale.
            poster (str): Poster image URL.

        Returns:
            Movie: The newly created movie instance.
        """
        movie = Movie(
            title=title,
            year=year,
            rating=rating,
            poster=poster,
            user_id=user_id
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, title, year, rating, poster):
        """
        Update an existing movie.

        Args:
            movie_id (int): Movie to update.
            title (str): New title.
            year (int): New release year.
            rating (float): New rating.
            poster (str): New poster URL.

        Returns:
            Movie | None: The updated movie, or ``None`` if not found.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = title
            movie.year = year
            movie.rating = rating
            movie.poster = poster
            db.session.commit()
        return movie

    def search_movies(self, query="", sort_by="title"):
        """
        Search for movies matching a query and sort order.

        Args:
            query (str, optional): Search substring applied to titles.
            sort_by (str): Sorting key (
            ``"title"``,
            ``"year"`` or
            ``"rating"``
            ).

        Returns:
            list[Movie]: Matching movies.
        """
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
        """
        Return the global movie catalogue with optional filters.

        Args:
            query (str, optional): Case-insensitive substring filter on the
                movie title.
            sort_by (str, optional): ``"title"``, ``"year"`` or ``"rating"``.

        Returns:
            list[Movie]: The filtered and/or sorted list of movies.
        """
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
        """
        Delete a movie from the database.

        Args:
            movie_id (int): Primary key of the movie to remove.

        Returns:
            bool: ``True`` if the movie existed and was deleted,
            ``False`` otherwise.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False

    def toggle_favorite(self, user_id: int, movie_id: int):
        fav = Favorite.query.filter_by(
            user_id=user_id,
            movie_id=movie_id
        ).first()
        if fav:
            db.session.delete(fav)
            added = False
        else:
            db.session.add(Favorite(user_id=user_id, movie_id=movie_id))
            added = True
        db.session.commit()
        return added
