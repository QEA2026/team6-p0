from flask import Flask, request, jsonify, current_app
from repository import (
    DatabaseConnection,
    User,
    UserRepository,
    Expense,
    ExpenseRepository
)
from service import AuthenticationService, ExpenseService

def create_app():
    app = Flask(__name__)

    # Configure Flask
    app.config['SECRET_KEY'] = 'your-secret-key-test'
    app.config['JSON_SORT_KEYS'] = False

    # Initialize database connection
    db_connection = DatabaseConnection()
    db_connection.initialize_database()

    # Initalize repositories
    user_repository = UserRepository(db_connection)
    expense_repository = ExpenseRepository(db_connection)

    # Initalize services
    jwt_secret_key = app.config['SECRET_KEY']  # Use Flask's secret key for JWT
    auth_service = AuthenticationService(user_repository, jwt_secret_key)
    expense_service = ExpenseService(expense_repository)


    # Inject service into flask app content
    app.auth_service = auth_service

    # POST 
    @app.route("/login", methods=['POST'])
    def login():
        """Employee login endpoint."""
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Request Body Required"}), 400

            # Check if user exits and password matches db
            username = data['username']
            password = data['password']

            user = auth_service.authenticate_user(username, password)

            # If user is valid, return jwt token
            if user:
                jwt_token = auth_service.generate_jwt_token(user)
                return jsonify(jwt_token)
            
            # User does not exist in the db
            return jsonify({"error": "Unauthorized"}), 401

        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
        
    # GET User from JWT token
    @app.route("/user", methods=['GET'])
    def get_user_from_jwt():
        """Get user from jwt token endpoint"""
        try: 
            # Authenticate User
            auth = request.headers.get("Authorization") # if missing, none

            if not auth or not auth.startswith("Bearer "):
                return jsonify({"errror": "Missing or malformed Authentication header"}), 401
            
            jwt_token = auth.split(" ", 1)[1]

            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            
            # Return user
            user = auth_service.get_user_from_token(jwt_token)

            if user:
                return jsonify(user)
            
            # User does not exist in the db
            return jsonify({"error": "Unauthorized"}), 401
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
        
    # POST expense to User ID
    @app.route("/expense", methods=['POST'])
    def insert_employee_expense():
        """Endpoint for the user to insert an expense."""
        try:
            # Validate body exists
            data = request.get_json()

            if not data:
                    return jsonify({"error": "Request Body Required"}), 400
            
            # Authenticate User
            auth = request.headers.get("Authorization")  # if missing, none

            if not auth or not auth.startswith("Bearer "):
                return jsonify({"errror": "Missing or malformed Authentication header"}), 401

            jwt_token = auth.split(" ", 1)[1]

            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            
            # Submit expense
            user_id = data['user_id']
            amount = data['amount']
            description = data['description']

            expense = expense_service.submit_expense(user_id, amount, description)
            return jsonify({"message":f"Successful Inserted Expense ID {expense.id}"})

        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
    
    # GET all expenses
    @app.route("/expense", methods=['GET'])
    def get_employee_expense_history():
        """Returns all expenses for the current user"""
        try:
            # Authenticate user
            auth = request.headers.get("Authorization")  # if missing, none

            if not auth or not auth.startswith("Bearer "):
                return jsonify({"errror": "Missing or malformed Authentication header"}), 401

            jwt_token = auth.split(" ", 1)[1]

            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            
            # Get user from token
            user = auth_service.get_user_from_token(jwt_token)

            if not user:
                return jsonify({"error": "Unauthorized"}), 401

            user_id = user.id

            # Return all expenses for the user
            expenses = expense_service.get_user_expenses(user_id)

            return jsonify(expenses)
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
        
    # GET expense by id
    @app.route("/expense/<expense_id>", methods=['GET'])
    def get_expense_by_id(expense_id):
        try: 
            # Authenticate user
            auth = request.headers.get("Authorization")  # if missing, none

            if not auth or not auth.startswith("Bearer "):
                return jsonify({"errror": "Missing or malformed Authentication header"}), 401

            jwt_token = auth.split(" ", 1)[1]

            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            
            # Get user from token
            user = auth_service.get_user_from_token(jwt_token)

            if not user:
                return jsonify({"error": "Unauthorized"}), 401
            
            # Get expense by id
            expense = expense_service.get_expense_by_id(expense_id, user.id)

            if not expense:
                return jsonify({"error": "Unauthorized or expense does not exist."}), 400
            
            return jsonify(expense)
            
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400

    # Patch existing employee expense
    @app.route("/expense", methods=['PATCH'])
    def patch_employee_expense():
        """Patches an expense record"""
        try:
            # Validate body exists
            data = request.get_json()

            if not data:
                return jsonify({"error": "Request Body Required"}), 400

            # Authenticate user
            auth = request.headers.get("Authorization")  # if missing, none

            if not auth or not auth.startswith("Bearer "):
                return jsonify({"errror": "Missing or malformed Authentication header"}), 401

            jwt_token = auth.split(" ", 1)[1]

            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            
            # Get updated expense fields
            user_id = data['user_id']
            expense_id = data['id']
            amount = data['amount']
            description = data['description']
            date = data['date']
            
            # Update and return expense
            updated_expense = expense_service.update_expense(expense_id, user_id, amount, description, date)
            return jsonify(updated_expense)

        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
        
    @app.route("/expense", methods=['DELETE'])
    def delete_employee_expense():
        try:
            # Validate body exists
            data = request.get_json()

            if not data:
                return jsonify({"error": "Request Body Required"}), 400

            # Authenticate user
            auth = request.headers.get("Authorization")  # if missing, none

            if not auth or not auth.startswith("Bearer "):
                return jsonify({"errror": "Missing or malformed Authentication header"}), 401

            jwt_token = auth.split(" ", 1)[1]

            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            
            expense_id = data['expense_id']
            user_id = data['user_id']
            
            result = expense_service.delete_expense(expense_id, user_id)

            if result == False:
                return jsonify({"error": "Failed to delete expense."}), 400
            
            return jsonify({"message": "Successfully deleted expense"})
            
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400

            
    return app
        


def create_sample_data():
    """Create a sample user for testing"""
    db_connection = DatabaseConnection()
    db_connection.initialize_database()

    user_repository = UserRepository(db_connection)

    # Create a sample employee user if it doesn't exist
    if not user_repository.find_by_username("e"):
        sample_employee = User(
            username="e",
            password="e",
            role="Employee"
        )
        user_repository.create(sample_employee)
        print("Created Sample Employee: employee1/password1")
        
if __name__ == "__main__":
        # Create app
    app = create_app()

    # Startup messages
    print("Starting Employee Management API...")
    print("Available endpoints:")
    print("POST /login - Employee login")

    # Fill with sample data
    create_sample_data()

    # Run app
    app.run(port=3000, debug=True)