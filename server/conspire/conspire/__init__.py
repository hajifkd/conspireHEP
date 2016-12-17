from flask import Flask, abort, session, request

import os
import functools

app = Flask(__name__)


def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not 'user_id' in session or not session['user_id']:
            abort(403)
        return f(*args, **kwargs)

    return wrapper


def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(32).encode('hex')
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token 

import conspire.views
