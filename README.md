# Uda-Spice Latte Cafe

## Full Stack Nano - IAM Final Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience. s a part of the Fullstack Nanodegree, it serves as a practice module for lessons from Course 2: API Development and Documentation by learning and applying skills to structure and implement well formatted API endpoints that leverage knowledge of HTTP and API development best practices. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 

```bash
export FLASK_APP=api.py
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

> View the [Backend README](./backend/README.md) for more details.

#### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. From the frontend folder, run the following commands to start the client: 

```bash
npm install // only once to install dependencies
npm install -g @ionic/cli
ionic serve
```

By default, the frontend will run on `http://127.0.0.1:8100/`.

> View the [Frontend README](./frontend/README.md) for more details.

### Tests

The endpoints are tested with [Postman](https://getpostman.com).

To run the tests:
- Import the postman collection `./udacity-fsnd-udaspicelatte-kidus.postman_collection`
- Run the collection

## API Reference

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: The app require authentication.

> View the [Backend README](./backend/README.md) for more details on each endpoints, authentication and guidlines.

## Deployment N/A

## Authors
The Udacity Team and yours truly, Kidus Worku

## Acknowledgements 
The awesome team at Udacity and the ALX-T community.
