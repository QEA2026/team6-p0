# Flask setup 
import traceback;
import requests;
import pandas as pd

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
                    user = requests.get("http://localhost:3000/user", headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})
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
                        print(f"Login Failed: {response.json()["error"]}")
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
            date = input("Enter Date (Press Enter to Skip): ")
            if date == "":
                date = None
            expense = requests.post("http://localhost:3000/expense", json={"user_id": user["id"], "amount": amount, "description": description, "date": date}, 
                                    headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})
            if(expense.ok):
                choice = None
                while choice != "1" or choice != "2":
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

def view_expenses(user, jwt_token):
    while True:
        clear_screen()
        print("=" * 12 + " Employee Expense Management App " + "=" * 12)
        print("=" * 12 + " EXPENSES " + "=" * 12)
        print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
        try:
            expenses = requests.get("http://localhost:3000/expense", headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})

            if (expenses.ok):
                while True:
                    clear_screen()
                    print("=" * 12 + " Employee Expense Management App " + "=" * 12)
                    print("=" * 12 + " EXPENSES " + "=" * 12)
                    print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
                    df = pd.DataFrame(expenses.json())
                    pd.set_option("display.float_format", "{:,.2f}".format)
                    df = df[["id", "amount", "description", "date"]]
                    print(df)
                    print("1. Update Expense")
                    print("2. Delete Expense")
                    print("3. Main Menu")
                    choice = input("Enter Selection: ")
                    if (choice == "1"):
                        update_expense(user, jwt_token)
                    elif (choice == "2"):
                        delete_expense(user, jwt_token)
                    elif (choice == "3"):
                        return
                    else:
                        print("Invalid selection. Try again.")
                        input("Press enter to continue.")
            else:
                clear_screen()
                print("=" * 12 + " Employee Expense Management App " + "=" * 12)
                print("=" * 12 + " EXPENSES " + "=" * 12)
                print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
                print("Error: " + expenses.json()["error"])
                print("Failed to display expenses.")
                input("Press enter to return to main menu.")
                return
        except:
            print("An error occurred! Please try again.")
            traceback.print_exc()
            input("Press enter to continue.")

def update_expense(user, jwt_token):
    while True:
        clear_screen()
        print("=" * 12 + " Employee Expense Management App " + "=" * 12)
        print("=" * 12 + " UPDATE EXPENSE " + "=" * 12)
        print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
        expense_id = input("Enter Expense ID: ")
        expense = requests.get(f"http://localhost:3000/expense/{expense_id}", 
                               headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"} )
        if expense.ok:
            while True:
                print(f"1: Amount - {expense.json()["amount"]}")
                print(f"2: Description - {expense.json()["description"]}")
                print(f"3: Date - {expense.json()["date"]}")
                choice = input("Enter Selection: ")
                if (choice == "1"):
                    break
                elif (choice == "2"):
                    return
                elif (choice == "3"):
                    return
                else:
                    print("Invalid selection. Try again.")
                    input("Press enter to continue.")
                
            input("Press enter to return to expenses.")
            return
        else:
            choice = None
            while choice != "1" or choice != "2":
                clear_screen()
                print("=" * 12 + " Employee Expense Management App " + "=" * 12)
                print("=" * 12 + " INSERT EXPENSE " + "=" * 12)
                print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
                print("Error: " + expense.json()["error"])
                print("Failed to update expense.")
                print("1. Retry Expense Update")
                print("2. Return to Expenses")
                choice = input("Enter Selection: ")
                if (choice == "1"):
                    break
                elif (choice == "2"):
                    return
                else:
                    print("Invalid selection. Try again.")
                    input("Press enter to continue.")

def delete_expense(user, jwt_token):
    return
            
def clear_screen():
    # ANSI: move cursor home + clear screen + clear scrollback
    print("\033[H\033[2J\033[3J", end="", flush=True)
        
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
            user = requests.get("http://localhost:3000/user", headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}).json()
            clear_screen()
            print("=" * 12 + " Employee Expense Management App " + "=" * 12)
            print("=" * 12 + " MAIN MENU " + "=" * 12)
            print("=" * 12 + f" USER: {user["username"]} " + "=" * 12)
            print("1. Insert Expense")
            print("2. View Expenses")
            print("3. Quit")
            choice = input("Enter Selection: ")
            if (choice == "1"):
                insert_expense(user, jwt_token)
            elif (choice == "2"):
                view_expenses(user, jwt_token)
            elif (choice == "3"):
                print("Goodbye!")
                break
            else:
                print("Invalid selection. Try again.")
                input("Press enter to continue.")



    
