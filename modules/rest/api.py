from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/api/")
def sample():
    """
    """

@api_blueprint.route("/api/register", methods=['GET'])
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
@api_blueprint.route("/api/verify-email/<verification_token>", methods=['POST'])
def verify_email(verification_token):
    # need to check token on database
    if verification_token == "valid_token":
        return jsonify({'message': 'Email verification successful'})
    else:
        return jsonify({'error': 'Invalid verification token'}), 400

@api_blueprint.route('/api/login', methods=['POST'])
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

@api_blueprint.route('/api/logout', methods=['POST'])
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


@api_blueprint.route('/api/password-recovery', methods=['POST'])
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
  
