from app import app
from database import db, Movie

with app.app_context():
    db.create_all()

    # Optional: Add Titanic if not already in DB
    if not Movie.query.first():
        titanic = Movie(
            title="Titanic",
            year=1997,
            rating=7.9,
            poster="https://m.media-amazon.com/images/M/MV5BYzYy...jpg"
        )
        db.session.add(titanic)
        db.session.commit()