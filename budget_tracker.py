import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

class BudgetTracker:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["budget_tracker"]
        self.expenses_collection = self.db["expenses"]
        self.categories_collection = self.db["categories"]
        self.income_collection = self.db["income"]

    def add_expense(self, amount, category):
        expense = {"amount": amount, "category": category}
        self.expenses_collection.insert_one(expense)

    def calculate_total_expense(self):
        total = sum(expense["amount"] for expense in self.expenses_collection.find())
        return total

    def set_income(self, income):
        self.income_collection.delete_many({})  # Remove any existing income entries
        self.income_collection.insert_one({"amount": income})

    def get_income(self):
        income_entry = self.income_collection.find_one()
        if income_entry:
            return income_entry["amount"]
        return 0

class BudgetTrackerGUI:
    def __init__(self, root):
        self.budget_tracker = BudgetTracker()

        self.root = root
        self.root.title("Budget Tracker")

        # Expense Amount
        self.amount_label = tk.Label(root, text="Expense Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        # Expense Category
        self.category_label = tk.Label(root, text="Expense Category:")
        self.category_label.grid(row=1, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add Expense Button
        self.add_expense_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Calculate Total Expense Button
        self.total_expense_button = tk.Button(root, text="Calculate Total Expense", command=self.calculate_total_expense)
        self.total_expense_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Income Label and Entry
        self.income_label = tk.Label(root, text="Set Income:")
        self.income_label.grid(row=4, column=0, padx=10, pady=10)
        self.income_entry = tk.Entry(root)
        self.income_entry.grid(row=4, column=1, padx=10, pady=10)

        # Set Income Button
        self.set_income_button = tk.Button(root, text="Set Income", command=self.set_income)
        self.set_income_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            self.budget_tracker.add_expense(amount, category)
            total_expense = self.budget_tracker.calculate_total_expense()
            income = self.budget_tracker.get_income()
            if total_expense > income:
                messagebox.showwarning("Warning", "Total expenses exceed the set income!")
            else:
                messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")

    def calculate_total_expense(self):
        total = self.budget_tracker.calculate_total_expense()
        messagebox.showinfo("Total Expense", f"Total Expense: ${total:.2f}")

    def set_income(self):
        try:
            income = float(self.income_entry.get())
            self.budget_tracker.set_income(income)
            messagebox.showinfo("Success", "Income set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid income amount")

def main():
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
