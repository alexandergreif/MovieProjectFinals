from app import app
from database import db
from database.models import User, Movie

with app.app_context():
    db.create_all()

    if not User.query.first():
        demo_user = User(name="Admin")
        db.session.add(demo_user)
        db.session.commit()

        movie = Movie(
            title="Titanic",
            year=1997,
            rating=7.9,
            poster="https://m.media-amazon.com/images/M/MV5BZTE2ZjE1MmYtNzhiMC00ZDZkLWEzYjAtM2M2NTM0YjMzMzAyXkEyXkFqcGc@._V1_.jpg_CR0,108,582,582_SX85_.jpg",
            user_id=demo_user.id
        )
        db.session.add(movie)
        db.session.commit()