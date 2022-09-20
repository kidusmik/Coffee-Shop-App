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

Or alternatively, execute:

```bash
export FLASK_APP=api.py
flask --reload
```
 
 The `--reload` flag will detect file changes and restart the server automatically.


## API Reference

### Getting Started
- Base URL: Currently the app can only be run locally and is not hosted at a base URL. The default backend host address is `127.0.0.1:5000`

- Authentication: The API requires authentication of users.

> NB: The Authorization token used here is a token for the role `Manager` and will expire on October 19, 2022

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

### Endpoints

#### GET /drinks
- Fetches a list of short representations of drinks.
- Request Arguments: None
- Returns: JSON object with two keys, `success` with value `True` and `drinks`, that contains a list of drinks.
- `curl 127.0.0.1:5000/drinks -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVYVRGaEd0ZHhMWE1EVk5XZy1yVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13MnhzcDN1Ni51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkwNzcwOTQyNDMxODUzNjY2MDkiLCJhdWQiOiJjb2ZmZWVzIiwiaWF0IjoxNjYzNTgxODU1LCJleHAiOjE2NjM2NjgyNTUsImF6cCI6ImhxQWxhVnVGRUVObjE5NGVMWkFxaVhXUmdjUGh6dlVOIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.UVwqwn2lfGNbP7-jnn8QqYKWZVdKcv3kYPok54OxKJS6ifkseUgdw3aXb9_fsgsQVhrMDwUSXvo7Auo71OLwz3qFE4T7L7X95-UkbBOeiEPb5Bgu-Jcmn90gxDEcstvPP8zBydKeI0hP1aq77hH4Zov09MoWO3KBrRzVZwUGV2Dx2JuPnfRF2fl8CRFZp6o5i9V0v-RqqCLB3wDHFNtMTR-8SmCrio7tyzziThKe_BR4O2OVG9iNNGsqmkA0nPyE8d-zAJ-iVDGBmKSghpDht9g0gMgbW0PbDphWfPpVwzpmdQCeey1rgHgwcpJE2STtQTZ9TYusDmMEx2t0qk44_Q"`

```json
{
  "drinks": [
    {
      "id": 1, 
      "recipe": [
        {
          "color": "blue", 
          "parts": 1
        }
      ], 
      "title": "water"
    }, 
    {
      "id": 2, 
      "recipe": [
        {
          "color": "grey", 
          "parts": 1
        }, 
        {
          "color": "brown", 
          "parts": 3
        }
      ], 
      "title": "Machiatto"
    }, 
    {
      "id": 3, 
      "recipe": [
        {
          "color": "brown", 
          "parts": 1
        }
      ], 
      "title": "Arabica"
    }, 
    {
      "id": 4, 
      "recipe": [
        {
          "color": "brown", 
          "parts": 1
        }, 
        {
          "color": "grey", 
          "parts": 1
        }
      ], 
      "title": "Espresso"
    }
  ], 
  "success": true
}
```

#### GET /drinks-details
- Fetches a list of long representations of drinks.
- Request Arguments:
  - token (str): The JWT token will be passed to be checked and verified
         if it is valid and contains the appropiriate permissions.
- Returns: JSON object with two keys, `success` with value `True` and `drinks`, that contains a list of drinks.
- `curl 127.0.0.1:5000/drinks-detail -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVYVRGaEd0ZHhMWE1EVk5XZy1yVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13MnhzcDN1Ni51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkwNzcwOTQyNDMxODUzNjY2MDkiLCJhdWQiOiJjb2ZmZWVzIiwiaWF0IjoxNjYzNTgxODU1LCJleHAiOjE2NjM2NjgyNTUsImF6cCI6ImhxQWxhVnVGRUVObjE5NGVMWkFxaVhXUmdjUGh6dlVOIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.UVwqwn2lfGNbP7-jnn8QqYKWZVdKcv3kYPok54OxKJS6ifkseUgdw3aXb9_fsgsQVhrMDwUSXvo7Auo71OLwz3qFE4T7L7X95-UkbBOeiEPb5Bgu-Jcmn90gxDEcstvPP8zBydKeI0hP1aq77hH4Zov09MoWO3KBrRzVZwUGV2Dx2JuPnfRF2fl8CRFZp6o5i9V0v-RqqCLB3wDHFNtMTR-8SmCrio7tyzziThKe_BR4O2OVG9iNNGsqmkA0nPyE8d-zAJ-iVDGBmKSghpDht9g0gMgbW0PbDphWfPpVwzpmdQCeey1rgHgwcpJE2STtQTZ9TYusDmMEx2t0qk44_Q"`

```json
{
  "drinks": [
    {
      "id": 1, 
      "recipe": [
        {
          "color": "blue", 
          "name": "water", 
          "parts": 1
        }
      ], 
      "title": "water"
    }, 
    {
      "id": 2, 
      "recipe": [
        {
          "color": "grey", 
          "name": "Milk", 
          "parts": 1
        }, 
        {
          "color": "brown", 
          "name": "Coffee", 
          "parts": 3
        }
      ], 
      "title": "Machiatto"
    }, 
    {
      "id": 3, 
      "recipe": [
        {
          "color": "brown", 
          "name": "Coffee", 
          "parts": 1
        }
      ], 
      "title": "Arabica"
    }, 
    {
      "id": 4, 
      "recipe": [
        {
          "color": "brown", 
          "name": "Coffee", 
          "parts": 1
        }, 
        {
          "color": "grey", 
          "name": "Milk", 
          "parts": 1
        }
      ], 
      "title": "Espresso"
    }
  ], 
  "success": true
}
```

#### POST /drinks
- Creates a new drink using the submitted `title` and `recipe` parameters.
- Request Arguments:
  - token (str): The JWT token will be passed to be checked and verified
         if it is valid and contains the appropiriate permissions.
- Returns: 
  - On Success: 
    - JSON object with two keys, `success` value of `True` and `ID` of the created drink.
  - On Failiure:
    - Aborts with http error code `422` if any of the paramters are missing or unsupported

- `curl 127.0.0.1:5000/drinks -X POST -H "Content-Type: application/json" -d '{"recipe": [{"color": "grey", "name": "Milk", "parts": 1}, {"color": "brown", "name": "Coffee", "parts": 3}], "title": "Machiatto"}' -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVYVRGaEd0ZHhMWE1EVk5XZy1yVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13MnhzcDN1Ni51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkwNzcwOTQyNDMxODUzNjY2MDkiLCJhdWQiOiJjb2ZmZWVzIiwiaWF0IjoxNjYzNTgxODU1LCJleHAiOjE2NjM2NjgyNTUsImF6cCI6ImhxQWxhVnVGRUVObjE5NGVMWkFxaVhXUmdjUGh6dlVOIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.UVwqwn2lfGNbP7-jnn8QqYKWZVdKcv3kYPok54OxKJS6ifkseUgdw3aXb9_fsgsQVhrMDwUSXvo7Auo71OLwz3qFE4T7L7X95-UkbBOeiEPb5Bgu-Jcmn90gxDEcstvPP8zBydKeI0hP1aq77hH4Zov09MoWO3KBrRzVZwUGV2Dx2JuPnfRF2fl8CRFZp6o5i9V0v-RqqCLB3wDHFNtMTR-8SmCrio7tyzziThKe_BR4O2OVG9iNNGsqmkA0nPyE8d-zAJ-iVDGBmKSghpDht9g0gMgbW0PbDphWfPpVwzpmdQCeey1rgHgwcpJE2STtQTZ9TYusDmMEx2t0qk44_Q"`

```json
{
  "created": 2, 
  "drinks": [
    {
      "id": 2, 
      "recipe": [
        {
          "color": "grey", 
          "name": "Milk", 
          "parts": 1
        }, 
        {
          "color": "brown", 
          "name": "Coffee", 
          "parts": 3
        }
      ], 
      "title": "Machiatto"
    }
  ], 
  "success": true
}
```

#### PATCH /drinks/{drink_id}
- Creates a new drink using the submitted `title` and `recipe` parameters.
- Request Arguments:
  - token (str): The JWT token will be passed to be checked and verified
         if it is valid and contains the appropiriate permissions.
  - drink_id (int): The ID of the drink to be deleted
- Returns: 
  - On Success: 
    - JSON object with two keys, `success` value of `True` and `ID` of the created drink.
  - On Failiure:
    - Aborts with http error code `404` if the `ID` of the drink isn't found
    - Aborts with http error code `422` if both the `title` and `recipe` paramaters are missing.
    
- `curl -X PATCH http://127.0.0.1:5000/drinks/1 -H "Content-Type: application/json" -d '{"title": "Not Water"}' -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVYVRGaEd0ZHhMWE1EVk5XZy1yVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13MnhzcDN1Ni51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkwNzcwOTQyNDMxODUzNjY2MDkiLCJhdWQiOiJjb2ZmZWVzIiwiaWF0IjoxNjYzNTgxODU1LCJleHAiOjE2NjM2NjgyNTUsImF6cCI6ImhxQWxhVnVGRUVObjE5NGVMWkFxaVhXUmdjUGh6dlVOIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.UVwqwn2lfGNbP7-jnn8QqYKWZVdKcv3kYPok54OxKJS6ifkseUgdw3aXb9_fsgsQVhrMDwUSXvo7Auo71OLwz3qFE4T7L7X95-UkbBOeiEPb5Bgu-Jcmn90gxDEcstvPP8zBydKeI0hP1aq77hH4Zov09MoWO3KBrRzVZwUGV2Dx2JuPnfRF2fl8CRFZp6o5i9V0v-RqqCLB3wDHFNtMTR-8SmCrio7tyzziThKe_BR4O2OVG9iNNGsqmkA0nPyE8d-zAJ-iVDGBmKSghpDht9g0gMgbW0PbDphWfPpVwzpmdQCeey1rgHgwcpJE2STtQTZ9TYusDmMEx2t0qk44_Q"`

```json
{
  "drinks": [
    {
      "id": 1, 
      "recipe": [
        {
          "color": "blue", 
          "name": "water", 
          "parts": 1
        }
      ], 
      "title": "Not Water"
    }
  ], 
  "success": true, 
  "updated": 1
}
```

#### DELETE /drinks/{drink_id}
- Deletes a drink using the submitted `id`.
- Request Arguments:
  - token (str): The JWT token will be passed to be checked and verified
         if it is valid and contains the appropiriate permissions.
  - drink_id (int): The ID of the drink to be updated
- Returns: 
  - On Success: 
    - JSON object with two keys, `success` value of `True` and `ID` of the deleted drink.
  - On Failiure:
    - Aborts with http error code `404` if the `ID` of the drink isn't found
    
- `curl -X DELETE http://127.0.0.1:5000/drinks/1 -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVYVRGaEd0ZHhMWE1EVk5XZy1yVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13MnhzcDN1Ni51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkwNzcwOTQyNDMxODUzNjY2MDkiLCJhdWQiOiJjb2ZmZWVzIiwiaWF0IjoxNjYzNTgxODU1LCJleHAiOjE2NjM2NjgyNTUsImF6cCI6ImhxQWxhVnVGRUVObjE5NGVMWkFxaVhXUmdjUGh6dlVOIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.UVwqwn2lfGNbP7-jnn8QqYKWZVdKcv3kYPok54OxKJS6ifkseUgdw3aXb9_fsgsQVhrMDwUSXvo7Auo71OLwz3qFE4T7L7X95-UkbBOeiEPb5Bgu-Jcmn90gxDEcstvPP8zBydKeI0hP1aq77hH4Zov09MoWO3KBrRzVZwUGV2Dx2JuPnfRF2fl8CRFZp6o5i9V0v-RqqCLB3wDHFNtMTR-8SmCrio7tyzziThKe_BR4O2OVG9iNNGsqmkA0nPyE8d-zAJ-iVDGBmKSghpDht9g0gMgbW0PbDphWfPpVwzpmdQCeey1rgHgwcpJE2STtQTZ9TYusDmMEx2t0qk44_Q"`

```json
{
  "deleted": 1, 
  "success": true
}
```

## Authentication Reference

The app uses Auth0 authentication, with `five` permissions and `two` roles.

### Permissions

   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`

### Roles

   - Barista
     - can `get:drinks-detail`
     - can `get:drinks`

   - Manager
     - can perform all actions

## Testing

The endpoints are tested with [Postman](https://getpostman.com).

To run the tests:
- Import the postman collection `./backend/udacity-fsnd-udaspicelatte.postman_collection.json`
- Run the collection

> NB: the Authorization tokens will expire on October 19, 2022
