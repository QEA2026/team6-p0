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
                        case "3" -> updateComment(expenseService, approvalDao);
                        case "4" -> reportsMenu(expenseService);
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

    private static void updateComment(ExpenseService expenseService, ApprovalDao approvalDao) {
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

    private static void reportsMenu(ExpenseService expenseService) {
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
                Integer userId = readInt("Employee user ID (blank to cancel): ");
                if (userId != null) {
                    printExpenses(expenseService.generateUserReport(userId));
                }
            }
            case "2" -> {
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