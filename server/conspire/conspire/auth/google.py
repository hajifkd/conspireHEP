import flask
import httplib2
import json

from conspire import app
from conspire.models import db, User, GoogleUser
from conspire.config import URL_PREFIX, REDIRECT_URL
from apiclient import discovery
from oauth2client import client

from sqlalchemy.orm.exc import NoResultFound

@app.route('/login-google')
def login_google():
    if 'credentials' not in flask.session:
        return flask.redirect(URL_PREFIX + flask.url_for('oauth_google'))

    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(URL_PREFIX + flask.url_for('oauth_google'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        userinfo_service = discovery.build('oauth2', 'v2', http_auth)
        userinfo = userinfo_service.userinfo().get().execute()

        if any(k not in userinfo for k in ('id', 'email', 'name')):
            flask.session['credentials'] = None
            return flask.redirect(URL_PREFIX + flask.url_for('login_google'))

        try:
            g_user = GoogleUser.query.filter_by(google_id=userinfo['id']).one()
            flask.session['user_id'] = g_user.user.id
        except NoResultFound:
            flask.session['user_tmp_data'] = {
                                               'google_id': userinfo['id'],
                                               'email': userinfo['email'],
                                               'username': userinfo['name'],
                                             }
            flask.session['user_type'] = 'google'
            return flask.redirect(URL_PREFIX + flask.url_for('signup'))

        return 'Login was successful. Please reload the page.'


@app.route('/oauth-google')
def oauth_google():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='openid profile email',
        redirect_uri=REDIRECT_URL)
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(URL_PREFIX + flask.url_for('login_google'))
