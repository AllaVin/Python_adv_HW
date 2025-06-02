from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # --- Связь: одна категория — много вопросов ---
    questions = db.relationship('Question', backref='category', lazy=True)


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    # --- Внешний ключ на категорию ---
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

