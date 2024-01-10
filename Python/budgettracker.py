import tkinter as tk
from tkinter import ttk, messagebox
import json


class BudgetTracker:
    def __init__(self, file_path="transactions.json"):
        self.file_path = file_path
        self.transactions = []
        self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.file_path, 'r') as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            pass

    def save_transactions(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.transactions, file, indent=2)

    def add_transaction(self, category, amount):
        transaction = {"category": category, "amount": amount}
        self.transactions.append(transaction)
        self.save_transactions()
        messagebox.showinfo("Info", "Transaction added successfully!")

    def calculate_remaining_budget(self, income):
        total_expenses = sum(transaction["amount"] for transaction in self.transactions if transaction["amount"] < 0)
        return income - total_expenses

    def analyze_expenses(self):
        expense_categories = {}
        for transaction in self.transactions:
            if transaction["amount"] < 0:
                category = transaction["category"]
                expense_categories[category] = expense_categories.get(category, 0) - transaction["amount"]
        return expense_categories


class BudgetTrackerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Budget Tracker")

        self.budget_tracker = BudgetTracker()

        self.income_label = ttk.Label(master, text="Monthly Income:")
        self.income_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.income_entry = ttk.Entry(master)
        self.income_entry.grid(row=0, column=1, padx=10, pady=10)
        self.income_entry.insert(0, "0.0")

        self.add_expense_button = ttk.Button(master, text="Add Expense", command=self.show_add_expense_window)
        self.add_expense_button.grid(row=1, column=0, pady=10)

        self.add_income_button = ttk.Button(master, text="Add Income", command=self.show_add_income_window)
        self.add_income_button.grid(row=1, column=1, pady=10)

        self.calculate_budget_button = ttk.Button(master, text="Calculate Remaining Budget", command=self.calculate_budget)
        self.calculate_budget_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.analyze_expenses_button = ttk.Button(master, text="Analyze Expenses", command=self.show_expense_analysis)
        self.analyze_expenses_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.exit_button = ttk.Button(master, text="Exit", command=self.master.destroy)
        self.exit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def show_add_expense_window(self):
        AddExpenseWindow(self.master, self.budget_tracker, self)

    def show_add_income_window(self):
        AddIncomeWindow(self.master, self.budget_tracker, self)

    def calculate_budget(self):
        try:
            income = float(self.income_entry.get())
            remaining_budget = self.budget_tracker.calculate_remaining_budget(income)
            messagebox.showinfo("Remaining Budget", f"Remaining Budget: ${remaining_budget:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid income value. Please enter a valid number.")

    def show_expense_analysis(self):
        expense_analysis = self.budget_tracker.analyze_expenses()
        ExpenseAnalysisWindow(self.master, expense_analysis)


class AddExpenseWindow:
    def __init__(self, master, budget_tracker, parent):
        self.master = master
        self.master.title("Add Expense")

        self.budget_tracker = budget_tracker
        self.parent = parent

        self.category_label = ttk.Label(master, text="Expense Category:")
        self.category_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.category_entry = ttk.Entry(master)
        self.category_entry.grid(row=0, column=1, padx=10, pady=10)

        self.amount_label = ttk.Label(master, text="Expense Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.amount_entry = ttk.Entry(master)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(master, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=1, pady=10)

    def add_expense(self):
        category = self.category_entry.get()
        try:
            amount = float(self.amount_entry.get())
            self.budget_tracker.add_transaction(category, -amount)
            self.master.destroy()
            self.parent.calculate_budget()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount value. Please enter a valid number.")


class AddIncomeWindow:
    def __init__(self, master, budget_tracker, parent):
        self.master = master
        self.master.title("Add Income")

        self.budget_tracker = budget_tracker
        self.parent = parent

        self.amount_label = ttk.Label(master, text="Income Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.amount_entry = ttk.Entry(master)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(master, text="Add Income", command=self.add_income)
        self.add_button.grid(row=1, column=1, pady=10)

    def add_income(self):
        try:
            amount = float(self.amount_entry.get())
            self.budget_tracker.add_transaction("Income", amount)
            self.master.destroy()
            self.parent.calculate_budget()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount value. Please enter a valid number.")


class ExpenseAnalysisWindow:
    def __init__(self, master, expense_analysis):
        self.master = master
        self.master.title("Expense Analysis")

        self.expense_analysis = expense_analysis

        self.listbox = tk.Listbox(master)
        self.listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.scrollbar = tk.Scrollbar(master, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.populate_listbox()

        self.ok_button = ttk.Button(master, text="OK", command=self.master.destroy)
        self.ok_button.grid(row=1, column=0, pady=10)

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for category, amount in self.expense_analysis.items():
            self.listbox.insert(tk.END, f"Category: {category}, Amount: ${amount:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()
