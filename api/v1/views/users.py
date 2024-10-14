#!/usr/bin/env python3
"""users endpoints"""
import json
from flask import request, abort, jsonify
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def view_all():
    """this views all the users in db"""
    all_user = [user.to_json() for user in User.all()]
    return jsonify(all_user)

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_a_user(user_id):
    """this gets a user"""
    if user_id is None:
        abort(400)

    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)      
    user = user[0]
    return jsonify(user.to_json())

@app_views.route('/users/', strict_slashes=False, methods=['DELETE'])
def del_user():
    """handles user deletion from database"""
    if request.current_user is None:
        abort(401)
    user = User.search({'id': request.current_user.id})
    if user is None:
        abort(404)
    if not user.remove():
        abort(400)
    return jsonify({})

@app_views.route('/users/', strict_slashes=False, methods=['PATCH'])
def update_user():
    """this view handles the updating of the user"""
    if request.current_user is None:
        abort(401)
    user = User.search({'id': request.current_user.id})
    if user is None:
        abort(401)
    to_be_updated = request.get_json()
    if to_be_updated is None or not to_be_updated:
        return jsonify({'Error': "No data provided"}), 400
    user.update(to_be_updated)
    return jsonify({'success': 'Profile successfully updated'}) 