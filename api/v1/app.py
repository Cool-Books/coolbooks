from flask import Flask, jsonify, request, abort, session
import os
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv
from flask_session import Session
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth

load_dotenv()

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"coolbooks/*": {"origins": "*"}})

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'oladevcoolbooks@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'oladevcoolbooks@gmail.com'
mail = Mail(app)

secret_key = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = secret_key

app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem for session store
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # Encrypt the session ID in the cookie
app.config['SESSION_FILE_DIR'] = './flask_session'  # Folder to store session files

Session(app)

auth = SessionAuth()

@app.before_request
def check_auth():
    """this function checks the authentication
    of the user before granting access to the user's request"""
    if not auth:
        return
    exc_path = ['/coolbooks/all_books/', '/coolbooks/login/',
                '/coolbooks/signup/', '/coolbooks/forgot_pwd/', '/coolbooks/reset_pwd/']

    if not auth.require_auth(request.path, exc_path):
        return
    
    if auth.session_cookie(request) is None:
        abort(403)

    user = auth.current_user(request)
    if user is None:
        abort(401)
    request.current_user = user

@app.errorhandler(ValueError)
def not_found(error):
    """handles 404"""
    return jsonify({
        'Error': str(error),
        'Status Code': 400,
    }), 400

@app.errorhandler(404)
def page_not_found(error):
    """handles 404"""
    return jsonify({"Error": "Page not found"})

@app.errorhandler(403)
def forbidden(error):
    """handles forbidden request"""
    return jsonify({'Error': "Forbidden"}), 403

@app.errorhandler(401)
def unauthorized(error):
    """handles unauthorized"""
    return jsonify({'Error': "Unauthorized"})

if __name__ == '__main__':
    app.run(debug=True)
