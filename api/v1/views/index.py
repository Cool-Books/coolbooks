#!/usr/bin/env python3
"""index views"""
import jwt
from flask import jsonify, make_response, request, current_app, abort
from api.v1.views import app_views
from models.book import Books
from models.user import User


@app_views.route('/signup', strict_slashes=False, methods=['POST'])
def sign_up():
    """this view handles sign up of the user"""
    data = request.get_json()
    if data is None or not data:
        return jsonify({'Error': "Invalid user"})
    pwd_confirm = data.get('password_confirm')
    pwd = data.get('password')
    if pwd_confirm != pwd:
        return ({'Error': 'Password do not match'})
    data.pop('password_confirm')
    new_user = User(**data)
    new_user.save()
    return jsonify({'success': "User created successfully"}), 200

@app_views.route('/login', strict_slashes=False, methods=['POST'])
def get_login():
    """this checks the login details"""
    from api.v1.app import auth
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email is None:
        raise ValueError("Email is missing")

    get_user = User.search({'email': email})
    if get_user is None or not get_user:
        return jsonify({"Error": "User not found"}), 404
    user = get_user[0]
    if not user.is_valid_pwd(password):
        return jsonify({'Error': "Invalid password"}), 401
    session_id = auth.create_session(user.id)
    response = make_response(jsonify({'message': "Login success"}))
    response.set_cookie("session_id", session_id)
    return response, 200

@app_views.route('/forgot_pwd', strict_slashes=False, methods=['POST'])
def forgot_password():
    """Allows user to request password reset"""
    from flask_mail import Message
    import os
    from datetime import datetime, timedelta
    from api.v1.app import mail

    email = request.json.get('email')
    if email is None:
        raise ValueError('Email is missing')
    get_user = User.search({'email': email})
    if get_user is None or not get_user:
        return jsonify({"Error": 'User not found'}), 404

    try:
        token = jwt.encode(
            {
                'reset_password': email,
                'exp': datetime.now() + timedelta(seconds=1800)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception:
        return jsonify({'Error': 'Error generating reset token'}), 500

    reset_url = f"http://localhost:5000/coolbooks/reset_pwd?token={token}"
    subject = "Password reset on CoolBooks"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd;">
            <h2 style="color: #333;">Password Reset Request</h2>
            <p>You're receiving this email because you requested a password reset for your user account at CoolBooks.</p>
            <p>Please click the button below to reset your password:</p>
            <div style="text-align: center; margin: 20px 0;">
                <a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a>
            </div>
            <p>If the button doesn't work, you can copy and paste the following link into your browser:</p>
            <p><a href="{reset_url}" style="color: #1a73e8;">{reset_url}</a></p>
            <p>Thanks for using CoolBooks!</p>
            <p>Best regards,<br>The CoolBooks Team</p>
        </div>
    </body>
    </html>
    """

    try:
        msg = Message(subject, sender=os.environ.get('MAIL_DEFAULT_SENDER'), recipients=[email])
        msg.html = html_content
        mail.send(msg)
        return jsonify({'Success': 'reset link sent successfully'}), 200
    except Exception:
        return jsonify({'Error': 'Error sending reset link'}), 500


@app_views.route('/logout', strict_slashes=False, methods=['GET'])
def logout():
    """handles logout"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200


@app_views.route('/reset_pwd', strict_slashes=False, methods=['POST'])
def reset_pwd():
    """handles reset password request"""
    token = request.args.get('token')
    if token is None:
        return jsonify({'Error': "Invalid request"}), 400
    new_pwd = request.json.get('new_password')

    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        email = data.get('email')
    except jwt.ExpiredSignatureError:
        return jsonify({'Error': 'Token has expired'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'Error': 'Invalid token'}), 400
    if new_pwd is None:
        return jsonify({'Error': "password cannot be empty"}), 400
    new_pwd_confirm = request.json.get('new_password_confirm')
    if new_pwd != new_pwd_confirm:
        return jsonify({'Error': "Passwords do not match"}), 400
    get_user = User.search({'email': email})
    if get_user is None or not get_user:
        return jsonify({'Error': "User not found"}), 404
    user = get_user[0]
    user.update({'password': new_pwd})
    return jsonify({'success': "Password reset successful"})


@app_views.route('/all_books', strict_slashes=False, methods=['GET'])
def get_allbooks():
    """displays all books"""
    all_book = [book.title for book in Books.all()]
    return jsonify(all_book)
