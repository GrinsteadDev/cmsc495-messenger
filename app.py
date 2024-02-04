import os
from flask import Flask, render_template, request, jsonify
from git import Repo
import jinja2
# Custom Modules located at ./modules/*
import modules.settings
import modules.rest.api

app = Flask(__name__)
app.register_blueprint(modules.rest.api.api_blueprint)

@app.route("/", defaults={ "name":"home", "ext":"html" })
@app.route("/<string:name>", defaults={ "ext":"" })
@app.route("/<string:name>.<string:ext>")
def fetch_templates(name, ext):
    # Fetches a template as a webpage url or returns 404
    if ext in ["", "html", "htm"] and not modules.settings.match_file_blacklist(name=f"{name}.*"):
        try:
            return render_template(f"{name}.html")
        except jinja2.exceptions.TemplateNotFound as e:
            pass
    
    return "", 404

@app.route("/git-push/", methods=['GET', 'POST'])
def update_repository():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Validation to make sure this is a webhook from git here
    # ...

    # Retrives the pull request for the current directory
    repo = Repo(curr_dir)
    repo.remotes.origin.pull()
    
    # Restarts the cPanel passeneger server
    if os.path.isfile(curr_dir + "/../tmp/restart.txt"):
        os.utime(curr_dir + "/../tmp/restart.txt", None)
    
    # Returns the 200 S_OK Status code
    return "", 200

@app.route("/api/register", methods=['GET', 'POST'])
def register_user():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    status = request.form.get('status')


    response = {
        'message': 'User registered successfully',
        'user_info': {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'status': status
        }
    }

    return jsonify(response)

# New route for email verification
@app.route("/api/verify-email/<verification_token>", methods=['POST'])
def verify_email(verification_token):
    # need to check token on database
    if verification_token == "valid_token":
        return jsonify({'message': 'Email verification successful'})
    else:
        return jsonify({'error': 'Invalid verification token'}), 400

@app.route('/api/login', methods=['POST'])
def user_login():
    # Get data from the form
    username = request.form.get('username')
    password = request.form.get('password')
    status = request.form.get('status')

    # Check credentials on database
    if username == 'demo' and password == 'password':
        response = {
            'message': 'Login successful',
            'user_info': {
                'username': username,
                'status': status
            }
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Invalid credentials'}), 401  # Unauthorized status code

@app.route('/api/logout', methods=['POST'])
def user_logout():

    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401  

    access_token = authorization_header.split(' ')[1]

    logout_message = request.form.get('message')

    # Logout logic 
    response = {
        'message': 'Logout successful',
        'logout_info': {
            'access_token': access_token,
            'logout_message': logout_message
        }
    }
    return jsonify(response)


@app.route('/api/password-recovery', methods=['POST'])
def password_recovery():
    user_email = request.form.get('email')

    # Perfrom user recovery, (recovery email and generate token)
    response = {
        'message': 'Password recovery email sent.',
        'user_info': {
            'email': user_email
        }
    }
    return jsonify(response)

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


if __name__ == "__main__":
    app.run()
