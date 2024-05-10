import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import datetime
import os

GOAL_FILE = "goal_amount.txt"


def save_goal():
    try:
        goal = float(goal_entry.get())
        with open(GOAL_FILE, "w") as file:
            file.write(str(goal))
        messagebox.showinfo("Success", "Goal amount saved successfully.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid goal amount.")


def load_goal():
    try:
        with open(GOAL_FILE, "r") as file:
            goal = float(file.read())
        goal_entry.insert(0, goal)
        messagebox.showinfo("Success", "Goal amount loaded successfully.")
    except FileNotFoundError:
        messagebox.showinfo("Info", "No goal amount saved yet.")
    except ValueError:
        messagebox.showerror("Error", "Invalid goal amount saved.")


def calculate():
    try:
        goal = float(goal_entry.get())
        rate = goal / 30  # Assuming 30 days in a month
        messagebox.showinfo("Result", f"You need to make ${rate:.2f} per day to reach your goal.")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid goal amount.")


def update_amount():
    try:
        amount = float(amount_entry.get())
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("money_log.txt", "a") as file:
            file.write(f"{date}: ${amount:.2f}\n")

        messagebox.showinfo("Success", "Amount updated and saved successfully.")
        amount_entry.delete(0, tk.END)
        plot_graph()

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")


def plot_graph():
    current_month = datetime.datetime.now().strftime("%B %Y")
    dates = []
    amounts = []
    with open("money_log.txt", "r") as file:
        for line in file:
            parts = line.strip().split(": ")
            date = datetime.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
            if date.strftime("%B %Y") == current_month:
                dates.append(parts[0])
                amounts.append(float(parts[1][1:]))  # Exclude dollar sign ($) from amount

    total_net = sum(amounts)
    plt.figure(figsize=(8, 5))
    plt.plot(dates, amounts, marker='o', linestyle='-')
    plt.title(f"Total Net for {current_month}")
    plt.xlabel('Date')
    plt.ylabel('Amount ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Adding goal amount to the corner
    if os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, "r") as file:
            goal = float(file.read())
            plt.text(0.02, 0.95, f"Goal: ${goal:.2f}", transform=plt.gca().transAxes, fontsize=10,
                     verticalalignment='top')

    plt.savefig('money_graph.png')
    plt.show()


def view_graph():
    plot_graph()


def delete_graph():
    if os.path.exists('money_graph.png'):
        os.remove('money_graph.png')
        messagebox.showinfo("Success", "Graph deleted successfully.")
    else:
        messagebox.showinfo("Info", "No graph to delete.")


# Create main window
root = tk.Tk()
root.title("Money Goal Tracker")

# Create labels and entries
goal_label = tk.Label(root, text="Enter your money goal:")
goal_label.pack()
goal_entry = tk.Entry(root)
goal_entry.pack()

# Load goal amount if it exists
load_goal_button = tk.Button(root, text="Load Goal", command=load_goal)
load_goal_button.pack()

calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.pack()

amount_label = tk.Label(root, text="Enter the amount made:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

update_button = tk.Button(root, text="Update Amount", command=update_amount)
update_button.pack()

view_graph_button = tk.Button(root, text="View Graph", command=view_graph)
view_graph_button.pack()

delete_graph_button = tk.Button(root, text="Delete Graph", command=delete_graph)
delete_graph_button.pack()

save_goal_button = tk.Button(root, text="Save Goal", command=save_goal)
save_goal_button.pack()

# Run the Tkinter event loop
root.mainloop()
