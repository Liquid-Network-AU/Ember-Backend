from flask import Flask, request, render_template, redirect, url_for, session
import requests

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

if __name__ == '__main__':
    app.run(debug=True)