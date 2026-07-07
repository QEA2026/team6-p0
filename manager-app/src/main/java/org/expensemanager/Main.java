package org.expensemanager;

import org.expensemanager.dao.ApprovalDao;
import org.expensemanager.dao.ApprovalDaoImpl;
import org.expensemanager.dao.ExpenseDao;
import org.expensemanager.dao.ExpenseDaoImpl;
import org.expensemanager.dao.UserDao;
import org.expensemanager.dao.UserDaoImpl;
import org.expensemanager.model.Approval;
import org.expensemanager.model.Expense;
import org.expensemanager.model.User;
import org.expensemanager.service.ExpenseService;
import org.expensemanager.service.UserService;

import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.NoSuchElementException;
import java.util.Scanner;

public class Main {

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        //wire up daos and services
        UserDao userDao = new UserDaoImpl();
        ExpenseDao expenseDao = new ExpenseDaoImpl();
        ApprovalDao approvalDao = new ApprovalDaoImpl();

        UserService userService = new UserService(userDao);
        ExpenseService expenseService = new ExpenseService(expenseDao, approvalDao, userDao);

        System.out.println("===  Expense Manager (Manager App) ===");

        try {
            User manager = login(userService);
            if (manager == null) {
                return; //user chose to quit at the login screen
            }
            System.out.println("\nWelcome, " + manager.getUsername() + "!");

            boolean running = true;
            while (running) {
                printMenu();
                String choice = scanner.nextLine().trim();
                //one bad action shouldn't kill the whole session:
                //catch anything unexpected and return to the menu
                try {
                    switch (choice) {
                        case "1" -> viewPending(expenseService);
                        case "2" -> reviewExpense(expenseService, manager);
                        case "3" -> updateComment(expenseService, expenseDao, approvalDao);
                        case "4" -> reportsMenu(expenseService, expenseDao, userDao);
                        case "5" -> running = false;
                        default -> System.out.println("Please enter a number from 1 to 5.");
                    }
                } catch (Exception e) {
                    System.out.println("Something went wrong: " + e.getMessage());
                    System.out.println("Returning to the menu.");
                }
            }
            System.out.println("Goodbye!");
        } catch (NoSuchElementException e) {
            //input stream was closed (e.g. Ctrl+D) - exit cleanly instead of crashing
            System.out.println("\nInput closed - exiting.");
        }
    }

    //loop until a manager logs in, or return null if they quit
    private static User login(UserService userService) {
        while (true) {
            System.out.print("\nUsername (or 'q' to quit): ");
            String username = scanner.nextLine().trim();
            if (username.equalsIgnoreCase("q")) {
                return null;
            }
            if (username.isEmpty()) {
                System.out.println("Username cannot be blank.");
                continue;
            }
            System.out.print("Password: ");
            String password = scanner.nextLine().trim();

            User user = userService.login(username, password);
            if (user == null) {
                System.out.println("Invalid username or password.");
            } else if (user.getRole() == null || !user.getRole().equalsIgnoreCase("manager")) {
                System.out.println("Access denied: this app is for managers only.");
            } else {
                return user;
            }
        }
    }

    private static void printMenu() {
        System.out.println("""

                ---- Manager Menu ----
                1. View pending expenses
                2. Approve or deny an expense
                3. Update a comment on a decision
                4. Reports
                5. Exit
                """);
        System.out.print("Choose an option: ");
    }

    private static void viewPending(ExpenseService expenseService) {
        ArrayList<Expense> pending = expenseService.viewPendingExpenses();
        if (pending == null || pending.isEmpty()) {
            System.out.println("No pending expenses to review.");
        } else {
            System.out.println("\nPending expenses:");
            printExpenses(pending);
        }
    }

    private static void reviewExpense(ExpenseService expenseService, User manager) {
        viewPending(expenseService);
        Integer expenseId = readInt("Expense ID to review (blank to cancel): ");
        if (expenseId == null) {
            return;
        }

        //keep asking until we get a valid decision, or blank to cancel
        String status;
        while (true) {
            System.out.print("Decision ('approved' or 'denied', blank to cancel): ");
            status = scanner.nextLine().trim();
            if (status.isEmpty()) {
                return;
            }
            if (status.equalsIgnoreCase("approved") || status.equalsIgnoreCase("denied")) {
                break;
            }
            System.out.println("Please type 'approved' or 'denied'.");
        }

        System.out.print("Comment for the employee: ");
        String comment = scanner.nextLine().trim();

        expenseService.reviewExpense(expenseId, status, manager.getId(), comment);
    }

    private static void updateComment(ExpenseService expenseService, ExpenseDao expenseDao, ApprovalDao approvalDao) {
        //only show expenses whose approval has been decided (approved/denied);
        //those are the only comments that can be edited
        ArrayList<Expense> all = expenseDao.getAllExpenses();
        if (all == null) {
            all = new ArrayList<>();
        }
        ArrayList<Expense> editable = new ArrayList<>();
        for (Expense e : all) {
            Approval a = approvalDao.getByExpenseId(e.getId());
            if (a != null && a.getStatus() != null && !a.getStatus().equalsIgnoreCase("pending")) {
                editable.add(e);
            }
        }
        if (editable.isEmpty()) {
            System.out.println("No reviewed expenses yet - approve or deny one first.");
            return;
        }
        System.out.println("\nExpenses you can edit the comment on:");
        printExpenses(editable);

        Integer expenseId = readInt("Expense ID whose comment you want to change (blank to cancel): ");
        if (expenseId == null) {
            return;
        }
        Approval approval = approvalDao.getByExpenseId(expenseId);
        if (approval == null) {
            System.out.println("No approval record found for that expense.");
            return;
        }
        if (approval.getStatus() == null || approval.getStatus().equalsIgnoreCase("pending")) {
            System.out.println("That expense hasn't been reviewed yet - approve or deny it first.");
            return;
        }
        System.out.println("Current comment: " + (approval.getComment() == null ? "(none)" : approval.getComment()));
        System.out.print("New comment (blank to cancel): ");
        String comment = scanner.nextLine().trim();
        if (comment.isEmpty()) {
            System.out.println("Comment unchanged.");
            return;
        }

        expenseService.updateComment(approval.getId(), comment);
        System.out.println("Comment updated.");
    }

    private static void reportsMenu(ExpenseService expenseService, ExpenseDao expenseDao, UserDao userDao) {
        System.out.println("""

                ---- Reports ----
                1. By employee
                2. By category
                3. By date range
                """);
        System.out.print("Choose a report: ");
        String choice = scanner.nextLine().trim();
        switch (choice) {
            case "1" -> {
                //show which users exist so the manager knows which id to pick
                printAllUsers(userDao);
                Integer userId = readInt("Employee user ID (blank to cancel): ");
                if (userId != null) {
                    printExpenses(expenseService.generateUserReport(userId));
                }
            }
            case "2" -> {
                //show which categories exist so the manager knows what to type
                printAllCategories(expenseDao);
                System.out.print("Category (blank to cancel): ");
                String category = scanner.nextLine().trim();
                if (!category.isEmpty()) {
                    printExpenses(expenseService.generateCategoryReport(category));
                }
            }
            case "3" -> {
                LocalDate start = readDate("Start date (YYYY-MM-DD, blank to cancel): ");
                if (start == null) {
                    return;
                }
                LocalDate end = readDate("End date (YYYY-MM-DD, blank to cancel): ");
                if (end == null) {
                    return;
                }
                if (start.isAfter(end)) {
                    System.out.println("Start date is after end date - no expenses to show.");
                    return;
                }
                printExpenses(expenseService.generateDateReport(start.toString(), end.toString()));
            }
            default -> System.out.println("Please enter 1, 2, or 3.");
        }
    }

    //lists every user so the manager knows which id to pick for a user report
    private static void printAllUsers(UserDao userDao) {
        ArrayList<User> users = userDao.getAllUsers();
        if (users == null || users.isEmpty()) {
            System.out.println("No users found.");
            return;
        }
        System.out.println("Users:");
        for (User u : users) {
            System.out.println("  " + u.getId() + " - " + u.getUsername() + " (" + u.getRole() + ")");
        }
    }

    //lists the distinct categories currently used by any expense
    private static void printAllCategories(ExpenseDao expenseDao) {
        ArrayList<Expense> all = expenseDao.getAllExpenses();
        if (all == null) {
            all = new ArrayList<>();
        }
        ArrayList<String> categories = new ArrayList<>();
        for (Expense e : all) {
            if (!categories.contains(e.getCategory())) {
                categories.add(e.getCategory());
            }
        }
        if (categories.isEmpty()) {
            System.out.println("No categories found.");
        } else {
            System.out.println("Available categories: " + categories);
        }
    }

    //prints a table of expenses; the service already explains empty results
    private static void printExpenses(ArrayList<Expense> expenses) {
        if (expenses == null || expenses.isEmpty()) {
            return;
        }
        System.out.printf("%-4s %-8s %-10s %-12s %-12s %s%n",
                "ID", "User", "Amount", "Category", "Date", "Description");
        for (Expense e : expenses) {
            System.out.printf("%-4d %-8d $%-9.2f %-12s %-12s %s%n",
                    e.getId(), e.getUserId(), e.getAmount(), e.getCategory(), e.getDate(), e.getDescription());
        }
    }

    //reads a whole number, reprompting on bad input; blank returns null to cancel
    private static Integer readInt(String prompt) {
        while (true) {
            System.out.print(prompt);
            String input = scanner.nextLine().trim();
            if (input.isEmpty()) {
                return null;
            }
            try {
                return Integer.parseInt(input);
            } catch (NumberFormatException e) {
                System.out.println("Please enter a whole number.");
            }
        }
    }

    //reads a real calendar date, reprompting on bad input; blank returns null to cancel
    private static LocalDate readDate(String prompt) {
        while (true) {
            System.out.print(prompt);
            String input = scanner.nextLine().trim();
            if (input.isEmpty()) {
                return null;
            }
            try {
                return LocalDate.parse(input);
            } catch (DateTimeParseException e) {
                System.out.println("Please use the format YYYY-MM-DD, e.g. 2026-07-07.");
            }
        }
    }
}