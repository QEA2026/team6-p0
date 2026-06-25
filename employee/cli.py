# Flask setup 
import subprocess;
import traceback;
import os;
import requests;

def login_page():        
        while True:
            clear_screen()
            print("=" * 12 + " Employee Expense Management " + "=" * 12)
            print("=" * 12 + " LOGIN PAGE " + "=" * 12)
            try:
                username = input("Enter Username: ")
                password = input("Enter Password: ")
                response = requests.post("http://localhost:3000/login", json={"username": username, "password": password})
                if(response.ok):
                    print("Login Successful!")
                    print(response.json())
                    input("Insert any key to return to menu.")
                    return
                else:
                    print(f"Login Failed: {response.json()}")
                    print("1. Login Page")
                    print("2. Main Menu")
                    choice = input("Enter Selection: ")
                    if(choice == "1"):
                        pass
                    elif(choice == "2"):
                        return
                    else:
                        print("Invalid selection. Try again.")
                        input("Insert any key to continue: ")
            except:
                print("An error occurred! Please try again.")
                traceback.print_exc()
                input("Insert any key to continue: ")
            
def clear_screen():
    # 'nt' is for Windows, 'posix' is for Linux/macOS
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        
if __name__ == "__main__":
    # Clear screen to start
    clear_screen()

    # Start command line menu
    while True:
        # clear screen for any 
        clear_screen()
        print("=" * 12 + " Employee Expense Management " + "=" * 12)
        print("=" * 12 + " MAIN MENU " + "=" * 12)
        print("1. Login")
        print("2. Quit")
        choice = input("Enter Selection: ")
        if(choice == "1"):
            login_page()
        elif(choice == "2"):
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Try again.")
            input("Insert any key to continue: ")

    
