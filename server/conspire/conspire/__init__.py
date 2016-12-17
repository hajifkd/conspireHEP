from flask import Flask, abort, session, request
import os

app = Flask(__name__)

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
