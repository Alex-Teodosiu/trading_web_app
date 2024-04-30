import functools
import requests

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        print(f"Email: {email}, Password: {password}")

        if not email or not password:
            return jsonify({'error': 'Username and password are required.'}), 400

        payload = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post('http://127.0.0.1:5000/users/signup', json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except requests.exceptions.ConnectionError as conn_err:
            print(f'Error connecting to the server: {conn_err}')
        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout error: {timeout_err}')
        except requests.exceptions.RequestException as err:
            print(f'An error occurred: {err}')

        if response.status_code == 200:
            try:
                response_json = response.json()
            except ValueError:
                return jsonify({'error': 'Invalid response from API server.'}), 500

            return redirect(url_for("auth.login"))
        else:
            try:
                response_json = response.json()
            except ValueError:
                return jsonify({'error': 'Invalid response from API server.'}), 500

            return jsonify(response_json), response.status_code
    else:
        return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')

        payload = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://127.0.0.1:5000/users/signin', json=payload, headers=headers)

        if response.status_code == 200:
            try:
                response_json = response.json()
                print(response_json)
            except ValueError:
                return jsonify({'error': 'Invalid response from API server.'}), 500

            session.clear()
            session['token'] = response_json['token'][0]['access_token']  
            return redirect(url_for('index'))
        else:
            try:
                response_json = response.json()
            except ValueError:
                return jsonify({'error': 'Invalid response from API server.'}), 500

            flash(response_json['error'])
    else:
        return render_template('auth/login.html')
    

    @bp.route('/user/<email>', methods=['GET'])
    def get_user(email):
        print(f"Email from URL: {email}")  # print email from URL

        print("Sending request to server...")  # print message before request

        response = requests.get(f'http://127.0.0.1:5000/users/getuser/{email}')

        print("Received response from server.")  # print message after request

        if response.status_code == 200:
            try:
                user = response.json()
            except ValueError:
                return jsonify({'error': 'Invalid response from API server.'}), 500
            return jsonify(user)
        else:
            try:
                response_json = response.json()
            except ValueError:
                return jsonify({'error': 'Invalid response from API server.'}), 500
            return jsonify(response_json), response.status_code

# bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    # else:
    #     g.user = get_db().execute(
    #         'SELECT * FROM user WHERE id = ?', (user_id,)
    #     ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Require Authentication in Other Views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view