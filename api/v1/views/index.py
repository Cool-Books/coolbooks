#!/usr/bin/env python3
"""index views"""
from crypt import methods
import jwt
from flask import (jsonify, make_response,
request, current_app, abort, url_for, render_template, redirect)
from api.v1.views import app_views
from models.book import Books
from models.user import User


@app_views.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
def sign_up():
    """
User sign-up endpoint
---
tags:
  - users
summary: Sign up a new user
description: Allows a user to sign up by providing their personal information.
parameters:
  - name: first_name
    in: body
    type: string
    required: true
    description: First name of the user
    example: John
  - name: last_name
    in: body
    type: string
    required: true
    description: Last name of the user
    example: Doe
  - name: email
    in: body
    type: string
    required: true
    description: Email address of the user
    example: johndoe@example.com
  - name: password
    in: body
    type: string
    required: true
    description: User password
    example: securepassword
  - name: password_confirm
    in: body
    type: string
    required: true
    description: Password confirmation
    example: securepassword
responses:
  200:
    description: User successfully created
    schema:
      type: object
      properties:
        success:
          type: string
          example: "User created successfully"
  400:
    description: Invalid or missing user data
    schema:
      type: object
      properties:
        Error:
          type: string
          example: "Invalid user"
  409:
    description: User already signed up
    schema:
      type: object
      properties:
        Error:
          type: string
          example: "You have already signed up"
    """

    if request.method == 'POST':
        data = request.get_json()
        if data is None or not data:
            return jsonify({'Error': "Invalid user"})
        data.pop('password_confirm')

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        try_user = User.search({'first_name': first_name, 'last_name': last_name, 'email': email})
        try:
            try_user = try_user[0]
            return jsonify({'Error': 'You have already signed up'}), 409
        except IndexError:
            pass

        new_user = User(**data)
        new_user.save()
        return jsonify({'success': "User created successfully"}), 200

    return render_template('signup.html')


@app_views.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def get_login():
    """
User login endpoint
---
tags:
  - users
summary: Login a user
description: Allows a user to log into the system.
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      required:
        - email
        - password
      properties:
        email:
          type: string
          example: "johndoe@example.com"
        password:
          type: string
          example: "securepassword"
responses:
  200:
    description: Login successful
    schema:
      type: object
      properties:
        success:
          type: string
          example: "Login success"
        redirect:
          type: string
          example: "/coolbooks/homepage"
  401:
    description: Invalid password
    schema:
      type: object
      properties:
        Error:
          type: string
          example: "Invalid password"
  404:
    description: User not found
    schema:
      type: object
      properties:
        Error:
          type: string
          example: "User not found"
  400:
    description: Missing email
    schema:
      type: object
      properties:
        Error:
          type: string
          example: "Email is missing"
    """

    from api.v1.app import auth
    if request.method == 'POST':
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
        response = make_response(jsonify({'success': "Login success", 'redirect': '/coolbooks/homepage'}))
        response.set_cookie("session_id", session_id)
        return response, 200
    return render_template('login.html')

@app_views.route('/forgot_pwd', strict_slashes=False, methods=['GET', 'POST'])
def forgot_password():
    """
Request password reset
---
tags:
  - users
summary: Send a password reset email
description: Sends a reset link to the provided email address.
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      required:
        - email
      properties:
        email:
          type: string
          example: "user@example.com"
responses:
  200:
    description: Reset link sent successfully
    schema:
      type: object
      properties:
        success:
          type: string
          example: "reset link sent successfully"
  400:
    description: Missing email
    schema:
      type: object
      properties:
        Error:
          type: string
          example: "Email is missing"
  404:
    description: User not found
    schema:
      type: object
      properties:
        Error:
          type: string
          example: "User not found"
  500:
    description: Token generation or mail sending failed
    schema:
      type: object
      properties:
        Error:
          type: string
          example: "Error sending reset link"
    """

    from flask_mail import Message
    import os
    from datetime import datetime, timedelta
    from api.v1.app import mail

    if request.method == 'POST':
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

        reset_url = f"http://localhost:5000/coolbooks/reset?token={token}"
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
            return jsonify({'success': 'reset link sent successfully'}), 200
        except Exception:
            return jsonify({'Error': 'Error sending reset link'}), 500
    return render_template('forget.html')

@app_views.route('/logout', strict_slashes=False, methods=['GET'])
def logout():
    """
Logs out the current user
---
tags:
  - users
summary: Logs out the currently authenticated user
description: Destroys the session of the authenticated user and logs them out.
parameters:
  - name: session_id
    in: cookie
    description: The session ID of the logged-in user
    required: true
    schema:
      type: string
      example: "abc123xyz456"
  - name: Authorization
    in: header
    description: Bearer token for user authentication (optional)
    required: false
    schema:
      type: string
      example: "Bearer token_value"
responses:
  200:
    description: Logout successful
    content:
      application/json:
        schema:
          type: object
          example: {}
  404:
    description: Logout failed (session not found)
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "Session not found"
    """

    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200


@app_views.route('/reset_pwd', strict_slashes=False, methods=['POST'])
def reset_pwd():
    """
Resets a user's password using a valid token
---
tags:
  - users
summary: Allows a user to reset their password using a valid JWT token.
description: This endpoint requires a valid reset token and new password details to reset a user's password.
parameters:
  - name: token
    in: query
    required: true
    description: JWT reset token sent to the user's email. It is used to authenticate the reset request.
    schema:
      type: string
      example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVkX3Byb2ZpbGUiOiJqb2huZG9lQGV4YW1wbGUuY29tIn0.abc123xyz"
  - name: new_password
    in: query
    required: true
    description: The new password that the user wants to set.
    schema:
      type: string
      example: "new_secure_password"
  - name: new_password_confirm
    in: query
    required: true
    description: Confirmation of the new password to ensure both fields match.
    schema:
      type: string
      example: "new_secure_password"
requestBody:
  required: false
responses:
  200:
    description: Password reset successful
    content:
      application/json:
        schema:
          type: object
          properties:
            success:
              type: string
              example: "Password reset successful"
  400:
    description: Invalid input or token errors
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "Passwords do not match"
  404:
    description: User not found
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "User not found"
  500:
    description: Error processing the password reset
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "Token has expired"
    """
    # Your actual code here...

    import bcrypt
    token = request.json.get('token')
    if token is None:
        return jsonify({'Error': "Invalid request"}), 400
    new_pwd = request.json.get('new_password')

    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        email = data.get('reset_password')
    except jwt.ExpiredSignatureError:
        return jsonify({'Error': 'Token has expired'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'Error': 'Invalid token'}), 400
    User.validate_pwd(new_pwd)
    hash_pwd = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_pwd_confirm = request.json.get('new_password_confirm')
    if new_pwd != new_pwd_confirm:
        return jsonify({'Error': "Passwords do not match"}), 400
    get_user = User.search({'email': email})
    if get_user is None or not get_user:
        return jsonify({'Error': "User not found"}), 404
    user = get_user[0]
    user.update({'password': hash_pwd})
    return jsonify({'success': "Password reset successful"})


@app_views.route('/all_books', strict_slashes=False, methods=['GET'])
def get_allbooks():
    """
Retrieves and returns a list of all books
---
tags:
  - books
summary: Display all available books
responses:
  200:
    description: A list of all books with their titles and cover image URLs
    content:
      application/json:
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
                example: "The Great Gatsby"
              cover:
                type: string
                example: "https://yourdomain.com/static/uploads/great_gatsby.jpg"
  500:
    description: Internal server error
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "Internal server error"
    """
    books = Books.all()
    all_books = [{
        'title': book.title,
        'cover': url_for('static', filename=f'uploads/{book.cover}', _external=True)  # Generate absolute URL
    } for book in books]

    return jsonify(all_books)


@app_views.route('/reset', strict_slashes=False, methods=['GET'])
def reset_to_html():
    """
Redirects to the HTML page with the token
---
tags:
  - users
summary: Redirect to the password reset HTML page with a token
parameters:
  - name: token
    in: query
    description: The token to validate the password reset request
    required: true
    schema:
      type: string
      example: "abcd1234efgh5678"
responses:
  200:
    description: Password reset HTML page with the provided token
    content:
      text/html:
        schema:
          type: string
          example: "<html>...</html>"
  400:
    description: Invalid token or missing token
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "Invalid token"
    """
    token = request.args.get('token')
    
    if token is None:
        return jsonify({'Error': 'Invalid token'}), 400
    
    # Render the reset.html page and pass the token to it
    return render_template("reset.html", token=token)


@app_views.route('/', strict_slashes=False, methods=['GET'])
def landing():
    """home page"""
    return render_template('landingpage.html')

@app_views.route('/popular', strict_slashes=False, methods=['GET'])
def popular():
    """popular html"""
    return render_template('popular.html')


@app_views.route('/top_rated', strict_slashes=False, methods=['GET'])
def top():
    """top rated"""
    return render_template('top_rated.html')

@app_views.route('/best_seller', strict_slashes=False, methods=['GET'])
def best_seller():
    """best_seller"""
    return render_template('best_seller.html')

@app_views.route('/action', strict_slashes=False, methods=['GET'])
def action():
    """action"""
    return render_template('action.html')

@app_views.route('/drama', strict_slashes=False, methods=['GET'])
def drama():
    """drama"""
    return render_template('drama.html')

@app_views.route('/romance', strict_slashes=False, methods=['GET'])
def romance():
    """romance"""
    return render_template('romance.html')

@app_views.route('/horror', strict_slashes=False, methods=['GET'])
def horror():
    """horror"""
    return render_template('horror.html')

@app_views.route('/thriler', strict_slashes=False, methods=['GET'])
def thriller():
    """thriller"""
    return render_template('thriller.html')

@app_views.route('/homepage', strict_slashes=False, methods=['GET'])
def home():
    """return the users homepage"""
    return render_template('user.html')