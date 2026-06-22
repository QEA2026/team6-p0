# Flask setup 

from flask import Flask, request, jsonify, current_app
from repository import (
    DatabaseConnection,
    User,
    UserRepository
)
from service import AuthenticationService

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
    
    # Initalize services
    jwt_secret_key = app.config['SECRET_KEY']  # Use Flask's secret key for JWT
    auth_service = AuthenticationService(user_repository, jwt_secret_key)

    # Inject service into flask app content
    app.auth_service = auth_service

    @app.route("/login", methods=['POST'])
    def login():
        """Employee login endpoint."""
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Authentication Required"}), 401

            # Check if user exits and password matches db
            username = data['username']
            password = data['password']

            user = auth_service.authenticate_user(username, password)

            if user:
                return jsonify(user)
            # User does not exist in the db
            return jsonify({"error": "Unauthorized"}), 401
            
        except:
            return jsonify({"error": "Bad Request"}), 400
        
    return app
        
def create_sample_data():
    """Create a sample user for testing"""
    db_connection = DatabaseConnection()
    db_connection.initialize_database()

    user_repository = UserRepository(db_connection)

    # Create a sample employee user if it doesn't exist
    if not user_repository.find_by_username("employee1"):
        sample_employee = User(
            id=None,
            username="employee1",
            password="password1",
            role="Employee"
        )
        user_repository.create(sample_employee)
        print("Created Sample Employee: employee1/password1")
        
if __name__ == "__main__":
    app = create_app()
    create_sample_data()

    print("Starting Employee Management API...")
    print("Available endpoints:")
    print("POST /login - Employee login")

    app.run(port=3000, debug=True)


    
