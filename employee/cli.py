# Flask setup 
import traceback;
import requests;
import pandas as pd
from datetime import datetime

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
                    page_header("LOGIN PAGE", user.json()["username"])
                    print("Login Successful!")
                    print(f"Welcome {user.json()["username"]}.")
                    input("Press enter to return to menu.")
                    return jwt_token
                else:
                    choice = None
                    while choice != "1" or choice != "2":
                        clear_screen()
                        page_header("LOGIN PAGE")
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
            amount = None
            # Validate user input for amount
            while amount == None:
                page_header("INSERT EXPENSE", user["username"], None, "AMOUNT")
                try:
                    amount = float(input("Enter Expense Amount: "))
                except ValueError:
                    input("Invalid number entered. Press enter to try again.")
            page_header("INSERT EXPENSE", user["username"], None, "DESCRIPTION")
            description = input("Enter Description: ")
            category = None
            while category == None:
                page_header("INSERT EXPENSE", user["username"], None, "CATEGORY")
                category = input("Enter Category: ")
                if category.strip().lower() not in ["supplies", "meals", "entertainment", "travel", "lodging", "other"]:
                    category = None
                    input("Invalid category. Please choose one of: Supplies, Meals, Entertainment, Travel, Lodging, Other. Press enter to try again.")

            date = None
            while date == None:
                page_header("INSERT EXPENSE", user["username"], None, "DATE")
                date = input("Enter Date (Press Enter to Skip): ")
                if date == "":
                    date = None
                    break
                if not validate_date(date):
                    date = None
                    input("Invalid date. Please use the format YYYY-MM-DD HH:MM:SS. Press enter to try again.")
            expense = requests.post("http://localhost:3000/expense", json={"user_id": user["id"], "amount": amount, "description": description, "category": category, "date": date}, 
                                    headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})
            if(expense.ok):
                choice = None
                while choice != "1" or choice != "2":
                    page_header("INSERT EXPENSE", user["username"])
                    print(expense.json()["message"])
                    print("1. Insert Additional Expense")
                    print("2. Main Menu")
                    choice = input("Enter Selection: ")
                    if (choice == "1"):
                        break
                    elif (choice == "2"):
                        return
                    else:
                        print("Invalid selection. Try again.")
                        input("Press enter to continue.")
            else:
                choice = None
                while choice != "1" or choice != "2":
                    page_header("INSERT EXPENSE", user["username"])
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
        page_header("EXPENSES", user["username"])

        try:
            expenses = requests.get("http://localhost:3000/expense", headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})

            if (expenses.ok):
                while True:
                    page_header("EXPENSES", user["username"])
                    if len(expenses.json()) == 0:
                        input("No expenses to display. Press Enter to return to main menu.")
                        return
                    df = pd.DataFrame(expenses.json())
                    pd.set_option("display.float_format", "{:,.2f}".format)
                    df = df[["id", "amount", "description", "date"]]
                    print(df)
                    print("1. Update Expense")
                    print("2. Delete Expense")
                    print("3. Main Menu")
                    choice = input("Enter Selection: ")
                    if (choice == "1"):
                        expense_id = None
                        while expense_id == None:
                            try:
                                expense_id = int(input("Enter Expense ID: "))
                            except ValueError:
                                input("Please enter a valid int. Press enter to try again.")
                        update_expense(user, jwt_token, expense_id)
                        break  # back to outer loop, re-fetches expenses
                    elif (choice == "2"):
                        expense_id = input("Enter Expense ID: ")
                        delete_expense(user, jwt_token, expense_id)
                        break  # back to outer loop, re-fetches expenses
                    elif (choice == "3"):
                        return
                    else:
                        print("Invalid selection. Try again.")
                        input("Press enter to continue.")
            else:
                page_header("EXPENSES", user["username"])
                print("Failed to display expenses.")
                input("Press enter to return to main menu.")
                return
        except:
            print("An error occurred! Please try again.")
            traceback.print_exc()
            input("Press enter to continue.")
            break

def update_expense(user, jwt_token, expense_id):
    while True:
        page_header("UPDATE EXPENSE", user["username"])
        expense = requests.get(f"http://localhost:3000/expense/{expense_id}",
                               headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})
        amount = expense.json()["amount"]
        description = expense.json()["description"]
        category = expense.json()["category"]
        date = expense.json()["date"]
        if expense.ok:
            while True:
                page_header("UPDATE EXPENSE", user["username"], expense_id)
                print(f"1: Amount - {amount}")
                print(f"2: Description - {description}")
                print(f"3: Category - {category}")
                print(f"4: Date - {date}")
                print("5: Return to Expenses")
                choice = input("Enter Selection: ")
                if (choice == "1"):
                    new_amount = None
                    while not new_amount:
                        try:
                            page_header("UPDATE EXPENSE", user["username"], expense_id, "AMOUNT")
                            new_amount = float(input("Enter updated amount: "))
                        except ValueError:
                            input("Please input a valid number. Press enter to try again.")
                    updated_expense = requests.patch("http://localhost:3000/expense",
                                   json={"user_id": user["id"], "id": expense_id, 
                                         "amount":new_amount, "description":description, "category": category, "date":date},
                                   headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})
                    if updated_expense.ok:
                        print("Updated Amount Successfully.")
                        input("Press enter to return to update page.")
                        break
                    else:
                        print("Failed to update amount.")
                        input("Press enter to return to update page.")
                        break
                elif (choice == "2"):
                    new_description = None
                    page_header("UPDATE EXPENSE",user["username"], expense_id, "DESCRIPTION")
                    new_description = input("Enter updated description: ")

                    updated_expense = requests.patch("http://localhost:3000/expense",
                                                     json={"user_id": user["id"], "id": expense_id,
                                                           "amount": amount, "description": new_description, "category": category, "date": date},
                                                     headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})
                    if updated_expense.ok:
                        print("Updated Description Successfully.")
                        input("Press enter to return to update page.")
                        break
                    else:
                        print("Failed to update description.")
                        input("Press enter to return to update page.")
                        break
                elif (choice == "3"):
                    new_category = None
                    while not new_category:
                        page_header("UPDATE EXPENSE",
                                    user["username"], expense_id, "CATEGORY")
                        new_category = input("Enter updated category: ")
                        if new_category.strip().lower() not in ["supplies", "meals", "entertainment", "travel", "lodging", "other"]:
                            new_category = None
                            input("Invalid category. Please choose one of: Supplies, Meals, Entertainment, Travel, Lodging, Other. Press enter to try again.")

                    updated_expense = requests.patch("http://localhost:3000/expense",
                                                     json={"user_id": user["id"], "id": expense_id,
                                                           "amount": amount, "description": description, "category":new_category, "date": date},
                                                     headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})
                    if updated_expense.ok:
                        print("Updated Category Successfully.")
                        input("Press enter to return to update page.")
                        break
                    else:
                        print("Failed to update category.")
                        input("Press enter to return to update page.")
                        break
                elif (choice == "4"):
                    new_date = None
                    while not new_date:
                        page_header("UPDATE EXPENSE", user["username"], expense_id, "DATE")
                        new_date = input("Enter updated date: ")
                        if not validate_date(new_date):
                            new_date = None
                            input("Invalid date. Please use the format YYYY-MM-DD HH:MM:SS. Press enter to try again.")
                    updated_expense = requests.patch("http://localhost:3000/expense",
                                                     json={"user_id": user["id"], "id": expense_id,
                                                           "amount": amount, "description": description, "category": category, "date": new_date},
                                                     headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"})
                    if updated_expense.ok:
                        print("Updated Date Successfully.")
                        input("Press enter to return to update page.")
                        break
                    else:
                        print("Failed to update date.")
                        input("Press enter to return to update page.")
                        break
                elif (choice == "5"):
                    return
                else:
                    print("Invalid selection. Try again.")
                    input("Press enter to continue.")   
        else:
            choice = None
            while choice != "1" or choice != "2":
                page_header("UPDATE EXPENSE", user["username"])
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

def page_header(page_title, username=None, expense_id=None, field=None):
    clear_screen()
    print("=" * 12 + " Employee Expense Management App " + "=" * 12)
    print("=" * 12 + f" {page_title} " + "=" * 12)
    if username:
        print("=" * 12 + f" USER: {username} " + "=" * 12)
    if expense_id:
        print("=" * 12 + f" EXPENSE ID: {expense_id} " + "=" * 12)
    if field:
        print("=" * 12 + f" FIELD: {field} " + "=" * 12)
    return

def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def delete_expense(user, jwt_token, expense_id):
    delete_result = requests.delete("http://localhost:3000/expense", json={"expense_id":expense_id, "user_id":user["id"]}, headers={"Authorization": f"Bearer {jwt_token}"})
    if delete_result.ok:
        print(f"Expense ID: {expense_id} deleted successfully.")
        input("Press enter to return to expenses.")
    else:
        print(f"Expense ID: {expense_id} failed to delete.")
        input("Press enter to return to expenses.")
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
        page_header("WELCOME")
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
            page_header("MAIN MENU", user["username"])
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



    
