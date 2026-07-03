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
            if user:
                jwt_token = auth_service.generate_jwt_token(user)
                return jsonify(jwt_token)
            
            # User does not exist in the db
            return jsonify({"error": "Unauthorized"}), 401

        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
    
    @app.route("/user", methods=['POST'])
    def get_user_from_jwt():
        """Get user from jwt token endpoint"""
        try: 
            # Validate body exists
            data = request.get_json()

            if not data:
                return jsonify({"error": "Request Body Required"}), 400
            
            jwt_token = data['jwt_token']

            # Validate User Token
            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            
            user = auth_service.get_user_from_token(jwt_token)

            if user:
                return jsonify(user)
            
            # User does not exist in the db
            return jsonify({"error": "Unauthorized"}), 401
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
        
    @app.route("/expense", methods=['POST'])
    def insert_employee_expense():
        """Endpoint for the user to insert an expense."""
        try:
            # Validate body exists
            data = request.get_json()

            if not data:
                    return jsonify({"error": "Request Body Required"}), 400

            jwt_token = data['jwt_token']

            # Validate User Token
            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            
            user_id = int(data['user_id'])
            amount = float(data['amount'])
            description = data['description']

            expense = expense_service.submit_expense(user_id, amount, description)
            return jsonify({"message":f"Successful Inserted Expense ID {expense.id}"})

        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
    
    @app.route("/expense", methods=['GET'])
    def get_employee_expense_history():
        try:
            """Returns all expenses for the current user"""
            # Validate body exists
            data = request.get_json()

            if not data:
                return jsonify({"error": "Request Body Required"}), 400

            jwt_token = data['jwt_token']

            # Validate User Token
            validate = auth_service.validate_jwt_token(jwt_token)
            if not validate:
                return jsonify({"error": "Unauthorized"}), 401
            user_id = int(data['user_id'])

            expenses = expense_service.get_user_expenses(user_id)

            return jsonify(expenses)
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