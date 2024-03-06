import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import sqlite3

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, category, date):
        self.expenses.append({'date': date, 'amount': amount, 'category': category})

    def get_expenses_by_category(self):
        expenses_by_category = {}
        for expense in self.expenses:
            category = expense['category']
            amount = expense['amount']
            if category in expenses_by_category:
                expenses_by_category[category] += amount
            else:
                expenses_by_category[category] = amount
        return expenses_by_category

    def generate_report(self):
        expenses_by_category = self.get_expenses_by_category()
        categories = list(expenses_by_category.keys())
        amounts = list(expenses_by_category.values())

        plt.bar(categories, amounts)
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.title('Expense Report')
        plt.show()

def add_expense():
    try:
        amount = float(amount_entry.get())
        category = category_entry.get()
        date = datetime.datetime.strptime(date_entry.get(), "%Y-%m-%d").date()

        if date > datetime.date.today():
            messagebox.showerror("Error", "Invalid date! Please enter a date in the past.")
            return

        tracker.add_expense(amount, category, date)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        status_label.config(text="Expense added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount or date format!")

def generate_report():
    if not tracker.expenses:
        messagebox.showinfo("Info", "No expenses added yet!")
    else:
        tracker.generate_report()

def save_to_database():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (date TEXT, amount REAL, category TEXT)''')

    for expense in tracker.expenses:
        c.execute("INSERT INTO expenses VALUES (?, ?, ?)", (expense['date'], expense['amount'], expense['category']))

    conn.commit()
    conn.close()
    messagebox.showinfo("Info", "Expenses saved to database!")

def main():
    global tracker, amount_entry, category_entry, date_entry, status_label

    root = tk.Tk()
    root.title("Expense Tracker")

    tracker = ExpenseTracker()

    frame = ttk.Frame(root, padding="10")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Amount:").grid(column=0, row=0, sticky=tk.W)
    amount_entry = ttk.Entry(frame)
    amount_entry.grid(column=1, row=0, sticky=tk.W)

    ttk.Label(frame, text="Category:").grid(column=0, row=1, sticky=tk.W)
    category_entry = ttk.Entry(frame)
    category_entry.grid(column=1, row=1, sticky=tk.W)

    ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(column=0, row=2, sticky=tk.W)
    date_entry = ttk.Entry(frame)
    date_entry.grid(column=1, row=2, sticky=tk.W)

    ttk.Button(frame, text="Add Expense", command=add_expense).grid(column=0, row=3, columnspan=2, pady=10)

    ttk.Button(frame, text="Generate Report", command=generate_report).grid(column=0, row=4, columnspan=2)

    ttk.Button(frame, text="Save to Database", command=save_to_database).grid(column=0, row=5, columnspan=2)

    status_label = ttk.Label(frame, text="")
    status_label.grid(column=0, row=6, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()
