from app import app
from database import db
from database.models import User, Movie

with app.app_context():
    db.create_all()

    if not User.query.first():
        demo_user = User(name="Alex")
        db.session.add(demo_user)
        db.session.commit()

        movie = Movie(
            title="Titanic",
            year=1997,
            rating=7.9,
            poster="https://m.media-amazon.com/images/M/MV5BYzYy...jpg",
            user_id=demo_user.id
        )
        db.session.add(movie)
        db.session.commit()