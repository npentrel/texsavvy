from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
from secrets import LINKEDIN_KEY, LINKEDIN_SECRET
from runLatex import xelatex

app = Flask(__name__, static_url_path='')
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

linkedin = oauth.remote_app(
    'linkedin',
    consumer_key=LINKEDIN_KEY,
    consumer_secret=LINKEDIN_SECRET,
    request_token_params={
        'scope': 'r_emailaddress',
        'state': 'RandomString',
    },
    base_url='https://api.linkedin.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
)

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    if 'linkedin_token' in session:
        me = linkedin.get('people/~')
        # print (me.data) 
        # me2 = linkedin.get('people/~/location')
        # print (me2.data) 
        # me3 = linkedin.get('people/~/formatted-name')
        # print (me3.data) 
        # me4 = linkedin.get('people/~/headline')
        # print (me4.data) 
        # me5 = linkedin.get('people/~/summary')
        # print (me5.data) 
        # me6 = linkedin.get('people/~/specialties')
        # print (me6.data) 
        # me7 = linkedin.get('people/~/positions')
        # print (me7.data) 
        # me8 = linkedin.get('people/~/picture-url')
        # print (me8.data) 
        # me9 = linkedin.get('people/~/public-profile-url')
        print (me.data) 
        # return jsonify(me.data)
        return redirect(url_for('hello'))
    return redirect(url_for('login'))


@app.route('/hello')
def hello():
	return redirect(url_for('static', filename='hello.html'))

@app.route('/login')
def login():
    return linkedin.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('linkedin_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = linkedin.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['linkedin_token'] = (resp['access_token'], '')
    me = linkedin.get('people/~')
    return jsonify(me.data)


@linkedin.tokengetter
def get_linkedin_oauth_token():
    return session.get('linkedin_token')


def change_linkedin_query(uri, headers, body):
    auth = headers.pop('Authorization')
    headers['x-li-format'] = 'json'
    if auth:
        auth = auth.replace('Bearer', '').strip()
        if '?' in uri:
            uri += '&oauth2_access_token=' + auth
        else:
            uri += '?oauth2_access_token=' + auth
    return uri, headers, body

linkedin.pre_request = change_linkedin_query


if __name__ == '__main__':
    app.run()
    xelatex()
