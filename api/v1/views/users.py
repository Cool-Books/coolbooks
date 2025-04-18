#!/usr/bin/env python3
"""users endpoints"""
import json
from flask import request, abort, jsonify, render_template
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def view_all():
    """
Retrieve all users from the database
---
tags:
  - users
summary: Get a list of all users
description: Returns a list of all users stored in the database in JSON format.
responses:
  200:
    description: A list of user objects
    content:
      application/json:
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: "a1b2c3d4"
              email:
                type: string
                example: "jane.doe@example.com"
              username:
                type: string
                example: "janedoe"
              # Add any other fields returned by user.to_json()
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
    all_user = [user.to_json() for user in User.all()]
    return jsonify(all_user)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_a_user(user_id):
    """
Retrieve a single user by ID
---
tags:
  - users
summary: Get a specific user
description: |
  Fetches a user by their ID. If the ID is 'me', it returns the currently authenticated user.
parameters:
  - in: path
    name: user_id
    required: true
    description: The ID of the user to retrieve, or 'me' for the currently authenticated user
    schema:
      type: string
responses:
  200:
    description: User retrieved successfully
    content:
      application/json:
        schema:
          type: object
          properties:
            id:
              type: string
              example: "a1b2c3d4"
            email:
              type: string
              example: "jane.doe@example.com"
            username:
              type: string
              example: "janedoe"
            # Add more fields based on user.to_json()
  400:
    description: Bad request – user ID is missing
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "User ID is required"
  404:
    description: User not found or not authenticated
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "User not found"
    """
    if user_id is None:
        abort(400)

    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None or not user:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/', strict_slashes=False, methods=['DELETE'])
def del_user():
    """
Delete the currently authenticated user
---
tags:
  - users
summary: Delete your user account
description: |
  Deletes the account of the currently authenticated user. Requires the user to be logged in.
security:
  - bearerAuth: []  # Assuming token-based auth, customize if you're using a different method
responses:
  200:
    description: User account deleted successfully
    content:
      application/json:
        schema:
          type: object
          example: {}
  400:
    description: Failed to delete user
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "User deletion failed"
  401:
    description: Unauthorized – user not authenticated
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "Unauthorized access"
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
    """
    if request.current_user is None:
        abort(401)
    user = User.search({'id': request.current_user.id})
    if user is None:
        abort(404)
    if not user.remove():
        abort(400)
    return jsonify({})


@app_views.route('/users/<id>', strict_slashes=False, methods=['PATCH'])
def update_user(id):
    """
Update a user's information
---
tags:
  - users
summary: Update a user's profile
description: |
  Allows an authenticated user to update their own profile or an admin to update another user's profile using the user ID.
  Use `"me"` as the ID to update the current user's profile.
parameters:
  - in: path
    name: id
    schema:
      type: string
    required: true
    description: ID of the user to update (or 'me' to update the current user)
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        example:
          first_name: "John"
          last_name: "Doe"
          email: "john.doe@example.com"
responses:
  200:
    description: User profile updated successfully
    content:
      application/json:
        schema:
          type: object
          properties:
            success:
              type: string
              example: "Profile successfully updated"
  400:
    description: No data provided for update
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "No data provided"
  401:
    description: Unauthorized – user not authenticated or not found
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "Unauthorized"
    """

    if id == 'me':
        if request.current_user is None or not request.current_user:
            abort(401)
        user = User.search({'id': request.current_user.id})
    else:
        user = User.search({'id': id})
    user = user[0]
    
    if user is None:
        abort(401)
    to_be_updated = request.get_json()
    if to_be_updated is None or not to_be_updated:
        return jsonify({'Error': "No data provided"}), 400
    user.update(to_be_updated)
    return jsonify({'success': 'Profile successfully updated'}) 
