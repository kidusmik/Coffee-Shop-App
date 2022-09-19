# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Set up the Database

This app uses a simple database for interaction, simply uncomment the line:

```python
# db_drop_and_create_all()
```

This will initialize the database, only uncomment this the first time running the app and comment it out again so that it doesn't initialize it again which will drop and recreate the database.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `api.py` file. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](https://flask.palletsprojects.com/en/1.0.x/tutorial/factory/).

To run the server, execute:

```bash
flask run --reload
```

Or alternatively, execute:

```bash
export FLASK_APP=api.py
flask --reloadrun
```
 
 The `--reload` flag will detect file changes and restart the server automatically.


## API Reference

### Getting Started
- Base URL: Currently the app can only be run locally and is not hosted at a base URL. The default backend host address is `127.0.0.1:5000`

- Authentication: The API requires authentication of users.

### Error Handling

The API handles Authorization, Resource and Server errors.

#### Authorization Error Handling

The API will return these errors when authorization fails:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden

Errors are returned as JSON objects in the following format:

```json
{
    "success": false,
    "error": 400,
    "message": "Error decoding token headers."
}
```
```json
{
    "success": false,
    "error": 400,
    "message": "Unable to parse authentication token."
}
```
```json
{
    "success": false,
    "error": 400,
    "message": "Unable to find the appropriate key."
}
```
```json
{
    "success": false,
    "error": 400,
    "message": "Permissions not included in JWT."
}
```


```json
{
    "success": false,
    "error": 401,
    "message": "Authorization header is expected."
}
```
```json
{
    "success": false,
    "error": 401,
    "message": "Authorization header must start with 'Bearer'"
}
```
```json
{
    "success": false,
    "error": 401,
    "message": "Token not found."
}
```
```json
{
    "success": false,
    "error": 401,
    "message": "Authorization header must be bearer token."
}
```
```json
{
    "success": false,
    "error": 401,
    "message": "Authorization malformed."
}
```
```json
{
    "success": false,
    "error": 401,
    "message": "Token expired."
}
```
```json
{
    "success": false,
    "error": 401,
    "message": "Incorrect claims. Please, check the audience and issuer."
}
```


```json
{
    "success": false,
    "error": 403,
    "message": "Permission not found."
}
```

#### Resource Error Handling
The API will return these errors when resource request fails:
- 404: Resource could not be found
- 405: Method not allowed
- 422: Unprocessable

Errors are returned as JSON objects in the following format:

```json
{
    "success": false,
    "error": 404,
    "message": "resource could not be found"
}
```
```json
{
    "success": false,
    "error": 405,
    "message": "method not allowed"
}
```
```json
{
    "success": false,
    "error": 422,
    "message": "unprocessable"
}
```

#### Server Error Handling
The API will returns this error for server error:
- 500: Internal Server Error

Errors are returned as JSON objects in the following format:

```json
{
    "success": false,
    "error": 500,
    "message": "internal server error"
}
```
### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
     - can `get:drinks`
   - Manager
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
