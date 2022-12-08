from flask import Flask, request, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import auth

app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = os.environ['STORE_FOLDER']

# Establish a session
@app.route('/authenticate', methods=['POST'])
def authenticate():
    try:
        session['user_id'] = False
        if not 'username' in request.headers or not 'password' in request.headers:
            return jsonify({'authenticated': False}), 401
        # Run authentication
        authResponse = auth.login(request.headers['username'], request.headers['password'])
        if authResponse['status']:
            session['user_id'] = authResponse['uid']
            return jsonify({'authenticated': True}), 200
        else:
            return jsonify({'authenticated': False}), 401
    except Exception:
        return jsonify({'authenticated': False}), 500

# Add a new file to the directory
@app.route('/upload', methods=['POST'])
def upload():
    try:
        validation = file_authenticate(request, "write")
        if not validation[0]:
            return validation[1], validation[2]
        if 'file' not in request.files:
            return jsonify({'completed': False,'error': "File not specified"}), 400
        cat_id = validation[1]

        file = request.files['file']
        filename = secure_filename(file.filename)
        # Make the folder incase it doesn't exist
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + secure_filename(str(cat_id))), exist_ok=True)
        # Save the file to the folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + secure_filename(str(cat_id)), filename))
        return jsonify({'completed': True}), 200
    except Exception:
        return jsonify({'completed': False}), 500

# Get a list of accessible files
@app.route('/get_all', methods=['GET'])
def get_all():
    try:
        validation = file_authenticate(request, "read")
        if not validation[0]:
            return validation[1], validation[2]
        cat_id = validation[1]

        # Generate a list of accessible files
        file_list = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + secure_filename(str(cat_id))))
        return jsonify({'completed': True, 'file_list': file_list}), 200
    except Exception:
        return jsonify({'completed': False}), 500
    

# Get an individual file
@app.route('/get', methods=['GET'])
def get():
    try:
        validation = file_authenticate(request, "read")
        if not validation[0]:
            return validation[1], validation[2]
        if not 'file' in request.headers:
            return False, jsonify({'completed': False,'error': "Missing file"}), 400
        cat_id = validation[1]

        # Serve the file
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + secure_filename(str(cat_id))), secure_filename(request.headers['file']))
    except Exception:
        return jsonify({'completed': False}), 500

# Collection of helpers for authenticating when uploading or downloading files
def file_authenticate(request, rw):
    # Check there is an active session
    if not session['user_id']:
        return False, jsonify({'completed': False, 'error': "User not authenticated"}), 401
    # Check a category is specified
    if not 'category' in request.headers:
        return False, jsonify({'completed': False,'error': "Missing category"}), 400
    # Check the user is authorised to view/edit that category
    if not request.headers['category'] in auth.get_roles(session['user_id'], rw):
        return False, jsonify({'completed': False,'error': "User not authroised"}), 403
    cat_id = auth.get_role_id(request.headers['category'])
    if cat_id == -1:
        return jsonify({'completed': False,'error': "Category doesn't exist"}), 400
    return [True, cat_id]

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port='5000')