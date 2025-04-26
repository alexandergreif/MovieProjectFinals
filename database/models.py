from . import db  # this comes from database/__init__.py
from datetime import datetime



class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    poster = db.Column(db.String(500))
    favorite = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    movies = db.relationship("Movie", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

class Favorite(db.Model):
    __tablename__ = "favorite"
    user_id  = db.Column(db.Integer, db.ForeignKey("user.id"),  primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), primary_key=True)
    created  = db.Column(db.DateTime, default=datetime.utcnow)

# Beziehungen
User.favorites  = db.relationship(
    "Movie",
    secondary="favorite",
    backref="favorited_by",
    lazy="dynamic",
)