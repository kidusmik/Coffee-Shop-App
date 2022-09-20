"""
This is the "api" file.

The api file defines the endpoints of the app.
"""
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one drink row
'''
# db_drop_and_create_all()


@app.after_request
def after_request(response):
    """
    This is part of the CORS implementation and modifies the response after
    the request. This adds the Content-Type and Authorization headers and the
    also allowed request types.

    Arguments:
        response (obj): The response object which include response headers.

    Returns:
        response (obj): The modified response object.
    """
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers',
                         'GET, POST, PATCH, DELETE, OPTIONS')

    return response


# ROUTES

@app.route('/drinks')
def retrieve_drinks():
    """
    This is a GET request to retreives all drinks. This is a public
    endpoint and doesn't require any permision or authentication.

    Arguments:
        None

    Returns:
        JSON which includes:
            - success (boolean): Value of 'True'
            - drinks (list): Short representation of the retreived drinks

    Aborts with an http error code 404:
        - If there are no drinks
    """
    all_drinks = Drink.query.all()
    if not all_drinks:
        abort(404)
    drinks = [drink.short() for drink in all_drinks]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drink_details(token):
    """
    This is a GET request to retreive all the drink details. This requires
    authentication and only roles with the 'get:drinks-detail' can interact
    with this endpoint successfully otherwise will encounter an authorization
    error.

    Arguments:
        token (str): The JWT token will be passed to be checked and verified
         if it is valid and contains the appropiriate permissions.

    Returns:
        JSON which includes:
            - success (boolean): Value of 'True'
            - drinks (list): Long representation of the retreived drinks

    Aborts with an http error code 404:
        - If there are no drinks
    """
    all_drinks = Drink.query.all()
    if not all_drinks:
        abort(404)
    drinks = [drink.long() for drink in all_drinks]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(token):
    """
    This is a POST request to create a new drink. This requires authentication
     and only roles with the 'post:drinks' can interact with this endpoint
     successfully otherwise will encounter an authorization error.

    Arguments:
        token (str): The JWT token will be passed to be checked and verified
        if it is valid and contains the appropiriate permissions.

    Returns:
        JSON which includes:
            - success (boolean): Value of 'True'
            - drinks (list): Long representation of the created drink
            - created (int): The ID of the created string

    Aborts with an http error code 422:
        - If the drink title is empty or not provided
        - If the drink recipe is not a list or not provided
    """
    body = request.get_json()
    title = body.get('title', None)
    recipe_json = body.get('recipe', None)

    try:
        if title == '' or title is None\
                or recipe_json is None\
                    or not isinstance(recipe_json, list):
            raise ValueError

        recipe = json.dumps(recipe_json)
        drink = Drink(title=title, recipe=recipe)
        drink.insert()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()],
        'created': drink.id
    })


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_existing_drink(token, drink_id):
    """
    This is a PATCH request to update an existing drink. This requires
    authentication and only roles with the 'patch:drinks' can interact with
    this endpoint successfully otherwise will encounter an authorization error.

    Arguments:
        token (str): The JWT token will be passed to be checked and verified
        if it is valid and contains the appropiriate permissions.

        drink_id (int): the ID of the drink to be updated.

    Returns:
        JSON which includes:
            - success (boolean): Value of 'True'
            - drinks (list): Long representation of the updated drink
            - updated (int): The ID of the updated string

    Aborts with:
        An http error code 404:
            - If the requested drink is not found
        An http error code 422:
            - If both the drink title and recipe are not povided
    """
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        abort(404)
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    if title is None and recipe is None:
        abort(422)
    if title:
        drink.title = title
    if recipe:
        drink.recipe = json.dumps(recipe)
    drink.update()

    return jsonify({
        'success': True,
        'drinks': [drink.long()],
        'updated': drink.id
    })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):
    """
    This is a DELETE request to delete a drink. This requires authentication
     and only roles with the 'delete:drinks' can interact with this endpoint
     successfully otherwise will encounter an authorization error.

    Arguments:
        token (str): The JWT token will be passed to be checked and verified
        if it is valid and contains the appropiriate permissions.

        drink_id (int): the ID of the drink to be deleted.

    Returns:
        JSON which includes:
            - success (boolean): Value of 'True'
            - deleted (int): The ID of the deleted string

    Aborts with an http error code 404:
        - If the requested drink is not found
    """
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        abort(404)
    drink.delete()

    return jsonify({
        'success': True,
        'deleted': drink_id
    })


# Error Handling

@app.errorhandler(422)
def unporcessable(error):
    """
    This is http code 422 (unprocessable) error handler.

    Arguments:
        - error: error (obj): The error object which contains the error
                 information

    Returns:
        JSON representation of the error which include:
            - success (boolean): Value 'False'
            - error (int): The http error code which is 422
            - message (str): The description of the error
    """
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@app.errorhandler(405)
def not_found(error):
    """
    This is http code 405 (method not allowed) error handler.

    Arguments:
        - error (obj): The error object which contains the error information

    Returns:
        JSON representation of the error which include:
            - success (boolean): Value 'False'
            - error (int): The http error code which is 405
            - message (str): The description of the error
    """
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(500)
def not_found(error):
    """
    This is http code 500 (internal server error) error handler.

    Arguments:
        - error (obj): The error object which contains the error information

    Returns:
        JSON representation of the error which include:
            - success (boolean): Value 'False'
            - error (int): The http error code which is 500
            - message (str): The description of the error
    """
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


@app.errorhandler(404)
def not_found(error):
    """
    This is http code 404 (resource not found) error handler.

    Arguments:
        - error (obj): The error object which contains the error information

    Returns:
        JSON representation of the error which include:
            - success (boolean): Value 'False'
            - error (int): The http error code which is 404
            - message (str): The description of the error
    """
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'requested resource not found'
    }), 404


@app.errorhandler(AuthError)
def authentication_error(error):
    """
    This is the AuthError error handler, this handles the authentication
    errors, currently the app handles http error codes 400, 401 and 403

    Arguments:
        - error (obj): The error object which contains the error information

    Returns:
        JSON representation of the error which include:
            - success (boolean): Value 'False'
            - error (int): The authentication http error code
            - message (str): The description of the error
    """
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error.get('description')
    }), error.status_code
