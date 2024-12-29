## URL Host

- https://capstone-3lm8.onrender.com/

# Book Publisher Project

Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

## Project Motivation

The Book Publisher Project models a store that is responsible for creating books and managing and assigning authors to those books.

This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.

## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

- Variable and function names are clear.
- Endpoints are logically named.
- Code is commented appropriately.
- Secrets are stored as environment variables.

### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [Render](https://render.com/) is the cloud platform used for deployment

### Running Locally

#### Installing Dependencies

##### Python 3.10.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Auth0 Setup

You need to setup an Auth0 account.
Environment variables needed: (setup.sh)

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Choose your tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="casting-agency" # Create an API in Auth0
export CLIENT_ID='xxxxxx' # Add your client ID
```

##### Roles

Create roles for users under `Users & Roles` section in Auth0

- Publisher Assistant
  - Can view authors and books
- Publisher Director
  - All permissions a Publisher Assistant
  - Add an authors or books from the database
  - Modify authors or books
- Publisher Producer
  - All permissions a Publisher Director
  - Add or delete a books or authors from the database

##### Permissions

Following permissions should be created under created API settings.

- `get:authors`
- `get:books`
- `post:authors`
- `post:books`
- `patch:authors`
- `patch:books`
- `delete:authors`
- `delete:books`

##### Set JWT Tokens in `setup.sh`

Use the following link to create users and sign them in. This way, you can generate

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

After getting JWT Token, you need to setup Environment variables needed: (setup.sh)

```bash
export ASSISTANT_TOKEN='xxx' # Token for casting assistant
export DIRECTOR_TOKEN='xxx' # Token for casting director
export PRODUCER_TOKEN='xxx' # Token for executive producer
```

#### Running Tests

To run the unit tests

```bash
python test_app.py
```

#### Launching The App locally

1.  Initialize and activate a virtualenv:

    ```bash
    virtualenv --no-site-packages env_capstone
    source env_capstone/bin/activate
    ```

2.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Configure database path to connect local postgres database in `models.py`

        ```python
        database_path = "postgres://{}/{}".format('localhost:5432', 'capstone')
        ```

    **Note:** For default postgres installation, default user name is `postgres` with no password. Thus, no need to speficify them in database path. You can also omit host and post (localhost:5432). But if you need, you can use this template:

```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```

For more details [look at the documentation (31.1.1.2. Connection URIs)](https://www.postgresql.org/docs/9.3/libpq-connect.html)

4. Setup the environment variables for Auth0 under `setup.sh` running:
   ```bash
   source setup.sh
   ```
5. To run the server locally, execute:

   ```bash
   export FLASK_APP=app.py
   export FLASK_DEBUG=True
   export FLASK_ENVIRONMENT=debug
   flask run --reload
   ```

## API Documentation

### Models

There are two models:

- Book
  - title
  - release
- Author
  - name
  - age
  - gender

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": False,
    "error": 400,
    "message": "Bad Request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 404: Resource not found
- 422: Unprocessable

### Endpoints

#### GET /books

- Get all books

- Paginating at 10 records

- Require `get:books` permission

- Responds with a 404 error if have no book to show
- Responds with a 400 error if get another error

- **Example Request:** `curl 'http://localhost:5000/books'`

- **Expected Result:**
  ```json
  {
  	"books": [
  		{
  		"id": 1,
  		"release": "Sun, 14 Nov 2032 00:00:00 GMT",
  		"title": "book 1"
  		},
  		{
  		"id": 2,
  		"release": "Sun, 14 Nov 2032 00:00:00 GMT",
  		"title": "book 2"
  		},
  		...
  	],
  	"total-books": 10,
  	"success": true
  }
  ```

#### GET /authors

- Get all authors

- Paginating at 10 records

- Requires `get:authors` permission

- Responds with a 404 error if have no book to show
- Responds with a 400 error if get another error

- **Example Request:** `curl 'http://localhost:5000/authors'`

- **Expected Result:**
  ```json
  {
  	"authors": [
  		{
          "age": 23,
          "gender": "Male",
          "id": 3,
          "name": "Ken"
      	},
  		{
          "age": 12,
          "gender": "Female",
          "id": 4,
          "name": "May"
      	},
  		...
  	],
  	"success": true,
  	"total-authors": 10
  }
  ```

#### POST /books

- Creates a new book.

- Requires `post:books` permission

- Requires the title and release date.

- Responds with a 422 error if request data is missing fields
- Responds with a 400 error if get another error

- **Example Request:** (Create)
  ```bash
  curl --location --request POST 'http://localhost:5000/books' \
  	--header 'Content-Type: application/json' \
  	--data-raw '{
  		"title": "New book",
  		"release_date": "2032-11-14"
  	}'
  ```
- **Example Response:**
  ```bash
  "books": [
      {
          "id": 5,
          "release": "Sun, 14 Nov 2032 00:00:00 GMT",
          "title": "New book"
      }
  ],
  "success": true
  ```

#### POST /authors

- Creates a new author.

- Requires `post:authors` permission

- Requires the name, age and gender of the author.

- Responds with a 422 error if request data is missing fields
- Responds with a 400 error if get another error

- **Example Request:** (Create)
  ```json
  curl --location --request POST 'http://localhost:5000/authors' \
  	--header 'Content-Type: application/json' \
  	--data-raw '{
  		"name": "Adam",
  		"age": 30,
  		"gender": "Male"
      }'
  ```
- **Example Response:**
  ```json
  "authors": [
  	{
          "age": 30,
          "gender": "Male",
          "id": 3,
          "name": "Adam"
      }
  ],
  "success": true
  ```

#### DELETE /books/<int:id>

- Deletes the book with given id

- Require `delete:books` permission

- Responds with a 404 error if <id> is not found
- Responds with a 400 error if get another error

- **Example Request:** `curl --request DELETE 'http://localhost:5000/books/1'`

- **Example Response:**
  ```json
  {
    "deleted_book": 1,
    "success": true
  }
  ```

#### DELETE /authors/<int:id>

- Deletes the author with given id

- Require `delete:authors` permission

- Responds with a 404 error if <id> is not found
- Responds with a 400 error if get another error

- **Example Request:** `curl --request DELETE 'http://localhost:5000/authors/1'`

- **Example Response:**
  ```json
  {
    "deleted_author": 1,
    "success": true
  }
  ```

#### PATCH /books/<id>

- Updates the book where <id> is the existing book id

- Require `update:books` permission

- Update the corresponding fields for book with id <id>

- Responds with a 404 error if <id> is not found
- Responds with a 400 error if get another error

- **Example Request:**
  ```json
    curl --location --request PATCH 'http://localhost:5000/books/1' \
  	--header 'Content-Type: application/json' \
  	--data-raw '{
  		"title": "New title"
        }'
  ```
- **Example Response:**
  ```json
  {
    "success": true,
    "books": {
      "id": 1,
      "release_date": "Wed, 04 May 2016 00:00:00 GMT",
      "title": "New title"
    }
  }
  ```

#### PATCH /authors/<id>

- Updates the author where <id> is the existing author id

- Require `update:authors`

- Update the given fields for author with id <id>

- Responds with a 404 error if <id> is not found
- Responds with a 400 error if get another error

- **Example Request:**
  ```json
    curl --location --request PATCH 'http://localhost:5000/authors/1' \
  	--header 'Content-Type: application/json' \
  	--data-raw '{
  		"name": "New Name"
        }'
  ```
- **Example Response:**
  ```json
  {
    "success": true,
    "updated": {
      "age": 30,
      "gender": "Male",
      "id": 1,
      "name": "New Name"
    }
  }
  ```
