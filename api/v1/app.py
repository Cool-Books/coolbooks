from flask import Flask, jsonify, request, abort, session
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv
from flask_session import Session
from flasgger import Swagger
from flasgger import Swagger

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "CoolBooks API",
        "description": "Interactive documentation for all CoolBooks endpoints",
        "version": "1.0.0"
    },
    "basePath": "/"
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,   # include all routes
            "model_filter": lambda tag: True    # include all models
        }
    ],
    "static_url_path": "/flasgger_static",  # where Flasgger will serve its JS/CSS
    "swagger_ui": True,
    "specs_route": "/apidocs/"             # the UI page
}

from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth
import os

load_dotenv()

app = Flask(__name__)

# -- Register your existing blueprint --
app.register_blueprint(app_views)

# -- CORS, Mail, Sessions, etc. (unchanged) --
CORS(app, resources={r"/coolbooks/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER']   = os.getenv('UPLOAD_FOLDER')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAIL_SERVER']     = 'smtp.gmail.com'
app.config['MAIL_PORT']       = 465
app.config['MAIL_USERNAME']   = 'oladevcoolbooks@gmail.com'
app.config['MAIL_PASSWORD']   = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS']    = False
app.config['MAIL_USE_SSL']    = True
app.config['MAIL_DEFAULT_SENDER'] = 'oladevcoolbooks@gmail.com'
Mail(app)

app.config['SECRET_KEY']      = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE']    = 'filesystem'
app.config['SESSION_PERMANENT']= False
app.config['SESSION_USE_SIGNER']= True
app.config['SESSION_FILE_DIR'] = './flask_session'
Session(app)

auth = SessionAuth()

@app.before_request
def check_auth():
    """this function checks the authentication
    of the user before granting access to the user's request"""

    exc_path = [
        # your existing public API endpoints
        '/coolbooks/all_books/', '/coolbooks/login/',
        '/coolbooks/signup/', '/coolbooks/forgot_pwd/',
        '/coolbooks/reset*', '/static*', '/coolbooks/',
        # add these lines to let swagger through
        '/apidocs/',            # the UI
        '/apispec_1.json*',      # the JSON spec
        '/flasgger_static*'     # any swagger‐static assets
    ]
    if not auth or not auth.require_auth(request.path, exc_path):
        return
    if auth.session_cookie(request) is None:
        abort(403)
    user = auth.current_user(request)
    if user is None:
        abort(401)
    request.current_user = user

@app.teardown_appcontext
def tear(exception):
    """close the session"""
    from models import storage
    storage.close()

@app.errorhandler(ValueError)
def not_found(error):
    return jsonify({'Error': str(error), 'Status Code': 400}), 400

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"Error": "Page not found"}), 404

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'Error': "Forbidden"}), 403

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'Error': "Unauthorized"}), 401

# -------------------------
# Flasgger / Swagger setup
# -------------------------
swagger = Swagger(app, template=swagger_template, config=swagger_config)

if __name__ == '__main__':
    app.run(debug=True)
