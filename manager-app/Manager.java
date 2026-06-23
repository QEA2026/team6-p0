public class Manager {
    private int manager_id;
    private String username;
    private String password;
    public Manager(int manager_id, String username, String password ) {
        this.manager_id = manager_id; // look at to potentially have this automatically iterate
        this.username = username;
        this.password = password; // look at encypting this & adding pw requirements

    }

    public static Manager login(String username, String password){
        //query database, check if entered username and password match
        //return true return manager so we can use it, else if return , look at try catch to handle wrong pw and username etc
        return null;
    }
    public void viewExpenses(){
        //

    }
    public boolean reviewExpense(){
        return false;
    }
    public void addComments(){

    }
    public void generateReport(){

        }

}

