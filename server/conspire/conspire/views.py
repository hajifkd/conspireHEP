from flask import session, render_template, request

from conspire import app, csrf_protect, login_required
from conspire.models import db, User, GoogleUser
from conspire.auth import google
import conspire.functions

from sqlalchemy.orm.exc import NoResultFound

import re

EMAIL_REGEXP = re.compile(r'[^@]+@[^@]+\.[^@]+')

@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/signup')
def signup():
    print session['user_tmp_data']
    return render_template("register.html", tmp_user = session['user_tmp_data'])


def register_google(username, email):
    user = User()
    google_user = GoogleUser()
    user.username = username
    user.email = email
    google_user.google_id = session['user_tmp_data']['google_id']
    user.google_user = google_user
    db.session.add(user)
    db.session.add(google_user)
    db.session.commit()
    session['user_id'] = user.id


@app.route('/register', methods=["POST"])
def register():
    csrf_protect()
    username = request.form['username']
    email = request.form['email']
    if any(c in username for c in ',\'\"<>\\&%!') or\
       not EMAIL_REGEXP.match(email):
        return flask.redirect(flask.url_for('signup'))

    if session['user_type'] == "google":
        register_google(username, email)

    return render_template('registered.html', username=username)

