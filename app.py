import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Person,Book,Author, setup_db
from flask_cors import CORS
from auth import AuthError, requires_auth

# For paginating, 10 records each page
RESPONSE_PER_PAGE = 10

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    # Handle paginating, 10 records each page
    def paginate_data(request, data):
        page = request.args.get('page', 1, type=int)
        start_index = (page - 1) * RESPONSE_PER_PAGE
        end_index = start_index + RESPONSE_PER_PAGE

        formatted_data = [record.format() for record in data]
        result = formatted_data[start_index:end_index]
        return result

    @app.route('/')
    def get_greeting():
        excited = os.getenv['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"
    
    # Get my information
    @app.route('/person', methods=['GET'])
    def get_me():
        try:
            # Query all Person objects
            persons = Person.query.all()
            
            # Serialize the data
            persons_serialized = [
                {
                    "id": person.id, 
                    "name": person.name,  
                    "catchphrase": person.catchphrase  
                } 
                for person in persons
            ]

            # Return the response
            return jsonify({
                'success': True,
                'me': persons_serialized
            }), 200
        
        except Exception as e:
            print(f"Error: {e}")  # Log the error for debugging
            abort(500)  # Return a 500 Internal Server Error for unexpected issues

    # Get all authors data
    @app.route('/authors', methods=['GET'])
    @requires_auth(permission='get:authors')
    def get_authors(payload):
        try:
            authors = Author.query.all()
            paginated_authors = paginate_data(request, authors)

            if len(paginated_authors) == 0:
                abort(404)

            amount_authors = len(authors)
            return jsonify({
                'success': True,
                'authors': paginated_authors,
                'total-authors': amount_authors
            }), 200
        except Exception:
            abort(400)

    # Get all books data
    @app.route('/books', methods=['GET'])
    @requires_auth(permission='get:books')
    def get_books(payload):
        try:
            books = Book.query.all()
            paginated_books = paginate_data(request, books)

            if len(paginated_books) == 0:
                abort(404)

            amount_books = len(books)
            return jsonify({
                'success': True,
                'books': paginated_books,
                'total-books': amount_books
            }), 200
        except Exception as e:
            print(e)
            abort(400)

    # Create new authors
    @app.route('/authors', methods=['POST'])
    @requires_auth(permission='post:authors')
    def create_authors(payload):
        data = request.get_json()
        try:
            name = data['name']
            gender = data['gender']
            age = data['age']
        except Exception:
            abort(422)

        try:
            new_author = Author(name=name,
                              gender=gender,
                              age=age)
            new_author.insert()

            return jsonify({
                "success": True,
                "actors": [new_author.format()]
            }), 200
        except Exception:
            abort(400)

    # Create new books
    @app.route('/books', methods=['POST'])
    @requires_auth(permission='post:books')
    def create_books(payload):
        data = request.get_json()
        try:
            title = data['title']
            release = data['release']
        except Exception:
            abort(422)

        try:
            new_book = Book(title=title,
                              release=release)
            new_book.insert()

            return jsonify({
                "success": True,
                "book": [new_book.format()]
            }), 200
        except Exception as e:
            print(e)
            abort(400)

    # Update authors
    @app.route('/authors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:authors')
    def update_authors(payload, id):
        author = Author.query.get(id)
        if author is None:
            abort(404)

        request_data = request.get_json()

        name = request_data.get('name', None)
        gender = request_data.get('gender', None)
        age = request_data.get('age', None)

        if name:
            author.name = name
        if gender:
            author.gender = gender
        if age:
            author.age = age

        try:
            author.update()
            return jsonify({
                "success": True,
                "actors": [author.format()]
            }), 200
        except Exception:
            abort(400)

    # Update book
    @app.route('/books/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:books')
    def update_books(payload, id):
        book = Book.query.get(id)
        if book is None:
            abort(404)

        request_data = request.get_json()

        title = request_data.get('title', None)
        release = request_data.get('release', None)

        if title:
            book.title = title
        if release:
            book.release = release

        try:
            book.update()
            return jsonify({
                "success": True,
                "movies": [book.format()]
            }), 200
        except Exception:
            abort(400)

    # Delete author
    @app.route('/authors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:authors')
    def delete_authors(payload, id):
        author = Author.query.get(id)
        if author is None:
            abort(404)

        try:
            author.delete()
            return jsonify({
                "success": True,
                "deleted_author": author.id
            }), 200
        except Exception:
            abort(400)

    # Delete book
    @app.route('/books/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:books')
    def delete_books(payload, id):
        book = Book.query.get(id)
        if book is None:
            abort(404)

        try:
            book.delete()
            return jsonify({
                "success": True,
                "deleted_book": book.id
            }), 200

        except Exception:
            abort(400)

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
