# Flask setup 
import subprocess;
import traceback;
import os;
import requests;
import json

def login_page():        
        while True:
            clear_screen()
            print("=" * 12 + " Employee Expense Management App " + "=" * 12)
            print("=" * 12 + " LOGIN " + "=" * 12)
            try:
                username = input("Enter Username: ")
                password = input("Enter Password: ")
                response = requests.post("http://localhost:3000/login", json={"username": username, "password": password})
                if(response.ok):
                    jwt_token = response.json()
                    user = requests.post("http://localhost:3000/user", json={"jwt_token":jwt_token})
                    clear_screen()
                    print("=" * 12 + " Employee Expense Management App " + "=" * 12)
                    print("=" * 12 + " LOGIN " + "=" * 12)
                    print("=" * 12 + f" USER: {user.json()["username"]} " + "=" * 12)
                    print("Login Successful!")
                    print(f"Welcome {user.json()["username"]}.")
                    input("Press enter to return to menu.")
                    return jwt_token
                else:
                    choice = None
                    while choice != "1" or choice != "2":
                        clear_screen()
                        print("=" * 12 + " Employee Expense Management App " + "=" * 12)
                        print("=" * 12 + " LOGIN PAGE " + "=" * 12)
                        print(f"Login Failed: {response.json()}")
                        print("1. Retry Login")
                        print("2. Main Menu")
                        choice = input("Enter Selection: ")
                        if(choice == "1"):
                            break
                        elif(choice == "2"):
                            return None
                        else:
                            print("Invalid selection. Try again.")
                            input("Press enter to continue.")
            except:
                print("An error occurred! Please try again.")
                traceback.print_exc()
                input("Press enter to continue.")

def insert_expense(user, jwt_token):
        while True:
            clear_screen()
            print("=" * 12 + " Employee Expense Management App " + "=" * 12)
            print("=" * 12 + " INSERT EXPENSE " + "=" * 12)
            print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
            amount = None
            # Validate user input for amount
            while amount == None:
                try:
                    amount = float(input("Enter Expense Amount: "))
                except ValueError:
                    print("Invalid number entered. Try again.")
            description = input("Enter Description: ")
            expense = requests.post("http://localhost:3000/expense", json={"jwt_token": jwt_token, "user_id": user["id"], "amount": amount, "description": description})
            if(expense.ok):
                clear_screen()
                print("=" * 12 + " Employee Expense Management App " + "=" * 12)
                print("=" * 12 + " INSERT EXPENSE " + "=" * 12)
                print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
                print(expense.json()["message"])
                print("1. Insert Additional Expense")
                print("2. Main Menu")
                choice = input("Enter Selection: ")
                if (choice == "1"):
                    pass
                elif (choice == "2"):
                    return
                else:
                    print("Invalid selection. Try again.")
                    input("Press enter to continue.")
            else:
                choice = None
                while choice != "1" or choice != "2":
                    clear_screen()
                    print("=" * 12 + " Employee Expense Management App " + "=" * 12)
                    print("=" * 12 + " INSERT EXPENSE " + "=" * 12)
                    print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
                    print(f"Expense Insert Failed: {expense.json()}")
                    print("1. Retry Expense Insert")
                    print("2. Main Menu")
                    choice = input("Enter Selection: ")
                    if (choice == "1"):
                        break
                    elif (choice == "2"):
                        return
                    else:
                        print("Invalid selection. Try again.")
                        input("Press enter to continue.")

def view_expense_history(user, jwt_token):
    while True:
        clear_screen()
        print("=" * 12 + " Employee Expense Management App " + "=" * 12)
        print("=" * 12 + " EXPENSE HISTORY " + "=" * 12)
        print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
        try:
            expenses = requests.get("http://localhost:3000/expense", json={"jwt_token":jwt_token,"user_id":user["id"]})
            data = {}
            if(expenses.ok): 
                for e in expenses.json():
                    print(e)
                print("Successfully displayed expenses.")
                input("Press enter to return to main menu.")
                return
            else:
                clear_screen()
                print("=" * 12 + " Employee Expense Management App " + "=" * 12)
                print("=" * 12 + " EXPENSE HISTORY " + "=" * 12)
                print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
                print("Error: " + expenses.json()["error"])
                print("Failed to display expense history.")
                input("Press enter to return to main menu.")
                return
        except:
            print("An error occurred! Please try again.")
            traceback.print_exc()
            input("Press enter to continue.")
            
            
def clear_screen():
    # 'nt' is for Windows, 'posix' is for Linux/macOS
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        
if __name__ == "__main__":
    # Clear screen to start
    clear_screen()

    jwt_token = None

    # Start command line menu
    while True:
        # clear screen   
        clear_screen()
        print("=" * 12 + " Employee Expense Management App " + "=" * 12)
        print("=" * 12 + " MAIN MENU " + "=" * 12)
        if not jwt_token:
            print("1. Login")
            print("2. Quit")
            choice = input("Enter Selection: ")
            if(choice == "1"):
                jwt_token = login_page()
            elif(choice == "2"):
                print("Goodbye!")
                break
            else:
                print("Invalid selection. Try again.")
                input("Press enter to continue.")
        else: # Employee is logged in
            user = requests.post("http://localhost:3000/user", json={"jwt_token":jwt_token}).json()
            clear_screen()
            print("=" * 12 + " Employee Expense Management App " + "=" * 12)
            print("=" * 12 + " MAIN MENU " + "=" * 12)
            print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
            print("1. Insert Expense")
            print("2. View Expense History")
            print("3. Quit")
            choice = input("Enter Selection: ")
            if (choice == "1"):
                insert_expense(user, jwt_token)
            elif (choice == "2"):
                view_expense_history(user, jwt_token)
            elif (choice == "3"):
                print("Goodbye!")
                break
            else:
                print("Invalid selection. Try again.")
                input("Press enter to continue.")



    
