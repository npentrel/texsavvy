from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth
from secrets import LINKEDIN_KEY, LINKEDIN_SECRET
from runLatex import xelatex
from template import render
import json
from utils import linkedin_format

app = Flask(__name__, static_url_path='', template_folder='static')
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)
# current_dir = os.path.dirname(os.path.abspath(__file__))
# jinjja = Environment(loader=FileSystemLoader(current_dir), trim_blocks=True)

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
    return redirect(url_for('static', filename='index.html'))

def linkedin_info():
    if 'linkedin_token' in session:
        me = linkedin_data()
        
        print json.dumps(me.data)

        template = render_template('cv.html',
            name=me.data['formattedName'],
            tagline=me.data['headline'],
            email=me.data['emailAddress'],
            pictureUrl=me.data['pictureUrls']['values'][0],
            linkedin=me.data['publicProfileUrl'],
            jobs=me.data['positions']['values']
        )
        return template

    return redirect(url_for('login'))

@app.route('/cv')
def cv():
	return linkedin_info()

@app.route('/edit')
def edit():
    if 'linkedin_token' in session:
        me = linkedin_data()
        template = render_template('edit.html',
            jobs=me.data['positions']['values']
        )
        return template
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return linkedin.authorize(callback=url_for('authorized', _external=True))

@app.route('/latex')
def latex():
    if 'linkedin_token' in session:
        me = linkedin.get('people/~:(id,first-name,last-name,formatted-name,headline,email-address,picture-url,picture-urls::(original),public-profile-url,location,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),patents:(id,title,summary,number,status:(id,name),office:(name),inventors:(id,name),date,url),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer)')
        xelatex(me.data)
        return "PDF created"
    return redirect(url_for('login'))

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
    return redirect(url_for('cv'))

@linkedin.tokengetter
def get_linkedin_oauth_token():
    return session.get('linkedin_token')

def linkedin_data():
    return linkedin.get('people/~:(id,first-name,last-name,formatted-name,headline,email-address,picture-url,picture-urls::(original),public-profile-url,location,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),patents:(id,title,summary,number,status:(id,name),office:(name),inventors:(id,name),date,url),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer)')

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
    app.debug = True
    app.run()
