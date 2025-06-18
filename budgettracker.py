import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# === Step 1: Initialize the database ===
def init_db():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# === Step 2: Add a transaction (income or expense) ===
def add_transaction(t_type, amount, category):
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO transactions (type, amount, category, date)
        VALUES (?, ?, ?, ?)
    ''', (t_type, amount, category, date))
    conn.commit()
    conn.close()
    print(f"{t_type.capitalize()} of ₦{amount} added under '{category}'.")

# === Step 3: View monthly summary ===
def view_report():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()
    income = 0
    expenses = 0

    print("\n=== All Transactions ===")
    for row in rows:
        print(f"ID: {row[0]} | Type: {row[1]} | Amount: ₦{row[2]} | Category: {row[3]} | Date: {row[4]}")
        if row[1] == 'income':
            income += row[2]
        elif row[1] == 'expense':
            expenses += row[2]

    print("\n=== Summary ===")
    print(f"Total Income: ₦{income}")
    print(f"Total Expenses: ₦{expenses}")
    print(f"Balance: ₦{income - expenses}")
    conn.close()

# === Step 4: Show expense pie chart ===
def show_chart():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount) FROM transactions
        WHERE type="expense" GROUP BY category
    ''')
    data = cursor.fetchall()
    conn.close()

    if data:
        labels = [row[0] for row in data]
        values = [row[1] for row in data]
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title('Spending by Category')
        plt.axis('equal')  # Make the pie chart a circle
        plt.show()
    else:
        print("No expense data to display.")

# === Step 5: Clear all data from the database ===
def clear_all_data():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions')
    conn.commit()
    conn.close()
    print("✅ All transaction data has been cleared.")

# === Step 6: Main menu ===
def main():
    init_db()
    while True:
        print("\n=== Budget Tracker Menu ===")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Report")
        print("4. Show Spending Chart")
        print("5. Exit")
        print("6. Clear All Data")

        choice = input("Choose an option: ")

        if choice == '1':
            try:
                amount = float(input("Enter income amount (₦): "))
                category = input("Enter income category: ")
                add_transaction('income', amount, category)
            except ValueError:
                print("Invalid input.")
        elif choice == '2':
            try:
                amount = float(input("Enter expense amount (₦): "))
                category = input("Enter expense category: ")
                add_transaction('expense', amount, category)
            except ValueError:
                print("Invalid input.")
        elif choice == '3':
            view_report()
        elif choice == '4':
            show_chart()
        elif choice == '5':
            print("Goodbye!")
            break
        elif choice == '6':
            confirm = input("⚠️ Are you sure? This will delete all transaction data. (yes/no): ")
            if confirm.lower() == 'yes':
                clear_all_data()
            else:
                print("Cancelled.")
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()