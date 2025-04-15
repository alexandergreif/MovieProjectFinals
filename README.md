# 🎬 MoviWeb

MoviWeb is a personal movie collection web app built with Flask and SQLite. Users can add, edit, favorite, and manage movies, as well as switch between user accounts in a simple and stylish UI inspired by modern streaming platforms.

---

## 🚀 Features

- Add/edit/delete movies with posters, ratings, and release years
- Favorite movies displayed at the top
- User management with soft-deactivation
- Sort movies by title, year, or rating
- Dark mode Amazon Prime-style interface
- Flash messages and validation for smoother UX

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/moviweb.git
cd moviweb
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python init_db.py
```

This creates an `Admin` user and inserts the movie _Titanic_ into the database.

### 5. Run the application

```bash
python3 app.py
```

Then go to `http://127.0.0.1:5000` in your browser.

---

## 🧰 Tech Stack

- Python 3
- Flask
- Jinja2
- SQLite (via SQLAlchemy)
- Bootstrap 5
- Custom CSS

---

## 🗂 Project Structure

```
moviweb/
│
├── app.py
├── init_db.py
├── requirements.txt
├── database/
│   ├── __init__.py
│   ├── models.py
│   └── sqlite_data_manager.py
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── explore.html
│   ├── ...
└── ...
```

---

## 🙌 Acknowledgements

This project was built as a learning project with custom extensions for styling, usability, and data structure organization.

---

## 📬 Contact

If you have any questions or want to contribute, feel free to reach out via issues or pull requests.
