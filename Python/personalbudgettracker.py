import json
from datetime import datetime

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
        transaction = {"timestamp": str(datetime.now()), "category": category, "amount": amount}
        self.transactions.append(transaction)
        self.save_transactions()
        print("Transaction added successfully!")

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


class BudgetTrackerCLI:
    def __init__(self):
        self.budget_tracker = BudgetTracker()

    def run(self):
        while True:
            print("\n1. Add Expense")
            print("2. Add Income")
            print("3. Calculate Remaining Budget")
            print("4. Analyze Expenses")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.add_income()
            elif choice == "3":
                self.calculate_budget()
            elif choice == "4":
                self.show_expense_analysis()
            elif choice == "5":
                self.budget_tracker.save_transactions()
                print("Budget information saved. Exiting.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def add_expense(self):
        category = input("Enter expense category: ")
        try:
            amount = float(input("Enter expense amount: "))
            self.budget_tracker.add_transaction(category, -amount)
            print("Expense added successfully!")
        except ValueError:
            print("Invalid amount value. Please enter a valid number.")

    def add_income(self):
        try:
            amount = float(input("Enter income amount: "))
            self.budget_tracker.add_transaction("Income", amount)
            print("Income added successfully!")
        except ValueError:
            print("Invalid amount value. Please enter a valid number.")

    def calculate_budget(self):
        try:
            income = float(input("Enter monthly income: "))
            remaining_budget = self.budget_tracker.calculate_remaining_budget(income)
            print(f"Remaining Budget: ${remaining_budget:.2f}")
        except ValueError:
            print("Invalid income value. Please enter a valid number.")

    def show_expense_analysis(self):
        expense_analysis = self.budget_tracker.analyze_expenses()
        for category, amount in expense_analysis.items():
            print(f"Category: {category}, Amount: ${amount:.2f}")


if __name__ == "__main__":
    budget_cli = BudgetTrackerCLI()
    budget_cli.run()
