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


class GoogleUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
