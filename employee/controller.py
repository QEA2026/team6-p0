from datetime import datetime
from flask import Flask, request, jsonify, current_app
from repository import (
    DatabaseConnection,
    User,
    UserRepository,
    Expense,
    ExpenseRepository,
    Approval,
    ApprovalRepository
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
    approval_repository = ApprovalRepository(db_connection)

    # Initalize services
    jwt_secret_key = app.config['SECRET_KEY']  # Use Flask's secret key for JWT
    auth_service = AuthenticationService(user_repository, jwt_secret_key)
    expense_service = ExpenseService(expense_repository, approval_repository)


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

            # Check that user is an employee
            if user:
                if user.role != "Employee":
                    return jsonify({"error": "Unauthorized"}), 403

            # If user is valid, return jwt token
            if user:
                jwt_token = auth_service.generate_jwt_token(user)
                return jsonify(jwt_token)
            
            # User does not exist in the db
            return jsonify({"error": "Unauthorized"}), 401

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
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
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
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
            category = data['category']
            date = data['date']

            expense = expense_service.submit_expense(user_id, amount, description, category, date)
            return jsonify({"message":f"Successful Inserted Expense ID {expense.id}"})

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
    
    # GET all pending expenses
    @app.route("/expense/pending", methods=['GET'])
    def get_employee_pending_expense_history():
        """Returns all pending expenses for the current user"""
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
            expenses_approvals = expense_service.get_expense_history(user_id, "pending")

            return jsonify(expenses_approvals)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
        
    # GET all reviewed expenses
    @app.route("/expense/reviewed", methods=['GET'])
    def get_employee_reviewed_expense_history():
        """Returns all reviewed expenses for the current user"""
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
            expenses_approvals = expense_service.get_expense_history(user_id, "pending", True)

            return jsonify(expenses_approvals)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400
        
    # GET a pending expense by id
    @app.route("/expense/pending/<expense_id>", methods=['GET'])
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

            # Get expense with its approval status
            result = expense_service.get_expense_with_status(expense_id, user.id)

            if not result:
                return jsonify({"error": "Unauthorized or expense does not exist."}), 400

            expense, approval = result

            # Only pending expenses may be opened for editing
            if approval.status != 'pending':
                return jsonify({"error": "Cannot update expense that has been reviewed."}), 400

            return jsonify(expense)
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
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
            category = data['category']
            date = data['date']
            
            # Update and return expense
            updated_expense = expense_service.update_expense(expense_id, user_id, amount, description, category, date)

            if not updated_expense:
                return jsonify({"error": "Unauthorized or expense does not exist."}), 400
            
            return jsonify(updated_expense)

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
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

            if not result:
                return jsonify({"error": "Unauthorized or expense does not exist."}), 400
            
            return jsonify({"message": "Successfully deleted expense"})
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({"error": "Bad Request"}), 400

            
    return app

def create_sample_data():
    """Create a sample user for testing"""
    db_connection = DatabaseConnection()
    db_connection.initialize_database()

    user_repository = UserRepository(db_connection)
    expense_repository = ExpenseRepository(db_connection)
    approval_repository = ApprovalRepository(db_connection)

    # Create a sample manager user if it doesn't exist. Seed first so its id
    # can be used as the reviewer on already-reviewed employee expenses.
    manager = user_repository.find_by_username("manager")
    if not manager:
        manager = User(
            username="manager",
            password="123",
            role="Manager"
        )
        user_repository.create(manager)
        print("Created Sample Manager: manager/123")

    reviewer_id = manager.id

    # Create a sample employee user if it doesn't exist
    if not user_repository.find_by_username("john"):
        sample_employee = User(
            username="john",
            password="123",
            role="Employee"
        )
        user_repository.create(sample_employee)
        print("Created Sample Employee: john/123")

        # Seed a few expenses with varied approval statuses so the
        # expense history page has something to show.
        review_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sample_expenses = [
            # (amount, description, category, date, status, comment)
            (42.50, "Team lunch", "Meals", "2026-06-15 12:30:00", "approved", "Looks good"),
            (120.00, "Hotel night", "Lodging", "2026-06-18 20:00:00", "approved", "Approved for conference"),
            (15.75, "Office pens", "Supplies", "2026-06-20 09:00:00", "denied", "Missing receipt"),
            (60.00, "Client dinner", "Entertainment", "2026-06-22 19:00:00", "pending", None),
        ]

        for amount, description, category, date, status, comment in sample_expenses:
            expense = expense_repository.create(Expense(
                user_id=sample_employee.id,
                amount=amount,
                description=description,
                category=category,
                date=date
            ))
            # create() seeds a 'pending' approval; move reviewed ones off pending
            if status != "pending":
                approval_repository.update_status(
                    expense.id,
                    status,
                    reviewer_id=reviewer_id,
                    comment=comment,
                    review_date=review_date
                )
        print(f"Seeded {len(sample_expenses)} sample expenses for john")

    # Create a second sample employee user if it doesn't exist
    if not user_repository.find_by_username("bob"):
        second_employee = User(
            username="bob",
            password="123",
            role="Employee"
        )
        user_repository.create(second_employee)
        print("Created Sample Employee: bob/123")

        # Seed expenses with both pending and approved statuses
        review_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        second_expenses = [
            # (amount, description, category, date, status, comment)
            (250.00, "Flight to conference", "Travel", "2026-06-10 08:00:00", "approved", "Approved for Q3 conference"),
            (85.30, "Taxi fares", "Travel", "2026-06-11 18:45:00", "approved", "Reimbursed"),
            (45.00, "Team coffee run", "Meals", "2026-06-25 10:15:00", "pending", None),
            (300.00, "New monitor", "Equipment", "2026-06-28 14:00:00", "pending", None),
        ]

        for amount, description, category, date, status, comment in second_expenses:
            expense = expense_repository.create(Expense(
                user_id=second_employee.id,
                amount=amount,
                description=description,
                category=category,
                date=date
            ))
            # create() seeds a 'pending' approval; move reviewed ones off pending
            if status != "pending":
                approval_repository.update_status(
                    expense.id,
                    status,
                    reviewer_id=reviewer_id,
                    comment=comment,
                    review_date=review_date
                )
        print(f"Seeded {len(second_expenses)} sample expenses for bob")

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