from . import db  # this comes from database/__init__.py
from datetime import datetime


class Movie(db.Model):
    """
    SQLAlchemy model representing a movie.

    Attributes:
        id (int): Primary key.
        title (str): Movie title.
        year (int): Release year.
        rating (float): Rating on a 0–10 scale.
        poster (str): Poster image URL.
        favorite (bool): Global favourite flag (legacy).
        user_id (int): Foreign key to the owning :class:`User`.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    poster = db.Column(db.String(500))
    favorite = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        """Return a concise string representation for debugging."""
        return f"<Movie {self.title}>"


class User(db.Model):
    """
    SQLAlchemy model representing an application user.

    Attributes:
        id (int): Primary key.
        name (str): Unique display name.
        is_active (bool): Soft-delete flag.
        movies (list[Movie]): Relationship to the user's movies.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    movies = db.relationship("Movie", backref="user", lazy=True)

    def __repr__(self):
        """Return a concise string representation for debugging."""
        return f"<User {self.name}>"


class Favorite(db.Model):
    """
    Association table mapping a user to one of their favourite movies.

    Attributes:
        user_id (int): FK → :class:`User.id`, part of the composite PK.
        movie_id (int): FK → :class:`Movie.id`, part of the composite PK.
        created (datetime): Timestamp when the movie was marked as favourite.
    """
    __tablename__ = "favorite"
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"),  primary_key=True
    )
    movie_id = db.Column(
        db.Integer, db.ForeignKey("movie.id"), primary_key=True
    )
    created = db.Column(
        db.DateTime, default=datetime.utcnow
    )


User.favorites = db.relationship(
    "Movie",
    secondary="favorite",
    backref="favorited_by",
    lazy="dynamic",
)
