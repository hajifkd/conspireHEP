from flask_sqlalchemy import SQLAlchemy
from conspire import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80))

    google_user = db.relationship('GoogleUser', backref='user',
                                  uselist=False)
    reactions = db.relationship('Reaction', backref='user')
    comments = db.relationship('Comment', backref='user')


class GoogleUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arxiv_id = db.Column(db.String(20), unique=True, nullable=False)

    reactions = db.relationship('Reaction', backref='article')
    comments = db.relationship('Comment', backref='article')


class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    reaction_list = ['like', 'dislike', 'read_later']
    reaction = db.Column(db.Enum(*reaction_list))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.Text)

