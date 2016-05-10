from flask import Flask, redirect, url_for, session, request, jsonify, render_template, send_from_directory
from flask_oauthlib.client import OAuth
from secrets import LINKEDIN_KEY, LINKEDIN_SECRET
from runLatex import xelatex
from pdfy import pdfytxt
from template import render
import json
from utils import linkedin_format
from collections import defaultdict
import os
from werkzeug import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['pdf'])
app = Flask(__name__, static_url_path='', template_folder='static')
app.debug = True
app.secret_key = 'development'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

# add global jinja helper functions 
app.jinja_env.globals.update(linkedin_format=linkedin_format)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

def linkedin_info(form_data):
    if 'linkedin_token' in session:
        me = linkedin_data()

        template = render_template('cv.html',
            name=me['formattedName'],
            tagline=me['headline'],
            email=me['emailAddress'],
            pictureUrl=me['pictureUrls']['values'][0],
            linkedin=me['publicProfileUrl'],
            form_data=form_data
        )
        return template

    return redirect(url_for('login'))

@app.route('/cv')
def cv():
    with open('data.json', 'r') as f:
        file = json.loads(f.read())
	return linkedin_info(file)

@app.route('/edit')
def edit():
    print session
    if 'linkedin_token' in session:
        me = linkedin.get('people/~:(id,first-name,last-name,formatted-name,headline,email-address,picture-url,picture-urls::(original),public-profile-url,location,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),patents:(id,title,summary,number,status:(id,name),office:(name),inventors:(id,name),date,url),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer)')
    
        template = render_template('edit.html',
            jobs=me.data['positions']['values']
        )
        return template
    return redirect(url_for('login'))

@app.route('/form', methods=['POST'])
def form():
    form_data = {}
    jobs = defaultdict(dict)
    for i in request.form:
        if i[-1].isdigit():
            jobs[int(i[-1])][i[:-1]] = request.form[i]
        else:
            form_data[i] = request.form[i]

    # convert back to lists
    jobs = [jobs[job] for job in jobs]
    form_data['jobs'] = jobs

    with open('data.json', 'w') as f:
        json.dump(form_data, f)
    return redirect(url_for('cv'))

@app.route('/login')
def login():
    return linkedin.authorize(callback=url_for('authorized', _external=True))

@app.route('/latex')
def latex():
    if 'linkedin_token' in session:
        me = linkedin_data()
        xelatex(me)
        return send_from_directory('static', 'resume.pdf')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('linkedin_token', None)
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename("uploadedcv.pdf")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload',
                                    filename=filename))
    return '''
    <!doctype html>
<html lang="en">
<head>

  <meta charset="utf-8">
  <title>Texsavvy</title>

  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="css/normalize.css">
  <link rel="stylesheet" href="css/skeleton.css">
  <link rel="stylesheet" href="css/custom.css">
  <link rel="stylesheet" href="css/buttons.css">

  <link rel="icon" type="image/png" href="images/favicon.png">

</head>
<body>
        <h1 id="cent"> Upload LinkedIn Resume</h1>
    <div id="cent">
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file >
             <input type=submit value=Upload class="button-primary" id="loginButton">
             <a href="latex" class="button" id="loginButton"><i class="fa fa-download"></i> Generate CV</a>
        </form>
    </div>
    </body>
</html>

    '''


@app.route('/login/authorized')
def authorized():
    resp = linkedin.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['linkedin_token'] = (resp['access_token'], '')
    return redirect(url_for('edit'))

@linkedin.tokengetter
def get_linkedin_oauth_token():
    return session.get('linkedin_token')

def linkedin_data():
    data = pdfytxt(['pdfy.py', 'uploadedcv.pdf'])
    print data
    dataLinkedIn = linkedin.get('people/~:(id,first-name,last-name,formatted-name,headline,email-address,picture-url,picture-urls::(original),public-profile-url,location,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),patents:(id,title,summary,number,status:(id,name),office:(name),inventors:(id,name),date,url),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer)')
    data['pictureUrls'] = {}
    data['pictureUrls']['values'] = {}
    data['pictureUrls']['values'][0] = dataLinkedIn.data['pictureUrls']['values'][0]
    data['publicProfileUrl'] = dataLinkedIn.data['publicProfileUrl']

    # data['pictureUrls'] = {}
    # data['pictureUrls']['values'] = {}
    # data['pictureUrls']['values'][0] = ""
    # data['publicProfileUrl'] = ""
    # print data
    return data

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
