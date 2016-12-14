import flask
import httplib2
import json

from conspire import app
from conspire.models import db, User, GoogleUser
from apiclient import discovery
from oauth2client import client

from sqlalchemy.orm.exc import NoResultFound

@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/signup')
def signup():
    return 'Hello, world!'


@app.route('/login')
def login():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))

    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        userinfo_service = discovery.build('oauth2', 'v2', http_auth)
        userinfo = userinfo_service.userinfo().get().execute()

        if any(k not in userinfo for k in ('id', 'email', 'name')):
            flask.session['credentials'] = None
            return flask.redirect(flask.url_for('login'))

        try:
            g_user = GoogleUser.query.filter_by(google_id=userinfo['id']).one()
            flask.session['user'] = g_user.user
        except NoResultFound as e:
            flask.session['user_tmp_data'] = userinfo
            flask.session['user_type'] = 'google'
            return flask.redirect(flask.url_for('signup'))

        return json.dumps(files)


@app.route('/login-google')
def login_google():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='openid profile email',
        redirect_uri=flask.url_for('login_google', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('login'))
