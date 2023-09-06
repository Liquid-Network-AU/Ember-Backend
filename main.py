from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_restful import Api, Resource, reqparse
import requests
import supabase
import os
import uuid

app = Flask(__name__)
app.secret_key = '' # Set with JWT

SUPABASE_URL = ''
SUPABASE_API_KEY = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')

    # Send registration request to Supabase
    response = requests.post(
        f'{SUPABASE_URL}/auth/v1/signup',
        json={'email': email, 'password': password},
        headers={'apikey': SUPABASE_API_KEY}
    )

    if response.status_code == 200:
        # Registration successful
        return redirect(url_for('login'))
    else:
        # Handle registration error
        return render_template('error.html', message='Registration failed')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Send login request to Supabase
    response = requests.post(
        f'{SUPABASE_URL}/auth/v1/token?grant_type=password&email={email}&password={password}',
        headers={'apikey': SUPABASE_API_KEY}
    )

    if response.status_code == 200:
        # Login successful
        session['access_token'] = response.json()['access_token']
        return redirect(url_for('profile'))
    else:
        # Handle login error
        return render_template('error.html', message='Login failed')

@app.route('/profile')
def profile():
    if 'access_token' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('login'))

# Repo creation
api = Api(app)

# Initialize Supabase client
supabase_url = 'https://your-subabase-url.supabase.co'
supabase_key = 'your-supabase-api-key'
supabase_client = supabase.Client(supabase_url, supabase_key)

# Directory to store local copies of repositories
repo_dir = 'repos'

# Ensure the repo directory exists
if not os.path.exists(repo_dir):
    os.makedirs(repo_dir)

# Parser for request data
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('collaborators', type=list, default=[])
parser.add_argument('files', type=list, default=[])


class RepositoryResource(Resource):
    def post(self):
        args = parser.parse_args()

        # Create a new repository entry in Supabase
        repository_id = str(uuid.uuid4())
        repo_data = {
            'id': repository_id,
            'owner': args['username'],
            'collaborators': args['collaborators'],
            'files': args['files']
        }
        _, error = supabase_client.from_('repositories').upsert([repo_data], on_conflict=['id']).execute()

        if error:
            return {'message': 'Error creating repository in Supabase'}, 500

        # Create a local directory for the repository
        repo_path = os.path.join(repo_dir, repository_id)
        os.makedirs(repo_path)

        return {'repository_id': repository_id}, 201


class FileUploadResource(Resource):
    def post(self, repository_id):
        repo_path = os.path.join(repo_dir, repository_id)

        # Ensure the repository directory exists
        if not os.path.exists(repo_path):
            return {'message': 'Repository not found'}, 404

        files = request.files.getlist('files')

        for file in files:
            filename = file.filename
            file.save(os.path.join(repo_path, filename))

        # Update the Supabase repository entry with the new files
        repo_data = {
            'files': os.listdir(repo_path)
        }
        _, error = supabase_client.from_('repositories').upsert([repo_data], on_conflict=['id']).execute()

        if error:
            return {'message': 'Error updating repository in Supabase'}, 500

        return {'message': 'Files uploaded successfully'}, 201


# Add resources to the API
api.add_resource(RepositoryResource, '/repositories')
api.add_resource(FileUploadResource, '/repositories/<string:repository_id>/upload')

if __name__ == '__main__':
    app.run(debug=True)