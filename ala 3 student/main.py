import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import os

users = {}
feedback_data = []

# --- Utility Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                username, password = line.strip().split(",")
                users[username] = password

def save_user(username, password):
    with open("users.txt", "a") as f:
        f.write(f"{username},{hash_password(password)}\n")

# --- App Class ---
class FeedbackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Feedback System")
        self.root.geometry("600x400")
        self.root.configure(bg="#d0f0fd")  # sky blue

        load_users()
        self.create_login_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- Login Page ---
    def create_login_page(self):
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Arial", 20, "bold"), bg="#d0f0fd", fg="black").pack(pady=30)

        tk.Label(self.root, text="Username:", font=("Arial", 12, "bold"), bg="#d0f0fd", fg="black").pack()
        username_entry = tk.Entry(self.root, font=("Arial", 12))
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 12, "bold"), bg="#d0f0fd", fg="black").pack()
        password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        password_entry.pack(pady=5)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if users.get(username) == hash_password(password):
                self.username = username
                self.create_home_page()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")

        login_btn = tk.Button(self.root, text="Login", font=("Arial", 12, "bold"), bg="#00bfff", fg="black", command=login)
        login_btn.pack(pady=10)

        register_btn = tk.Button(self.root, text="Register", font=("Arial", 10, "bold"), bg="#ccc", fg="black", command=self.create_register_page)
        register_btn.pack()

    # --- Register Page ---
    def create_register_page(self):
        self.clear_window()
        tk.Label(self.root, text="Register", font=("Arial", 20, "bold"), bg="#d0f0fd", fg="black").pack(pady=30)

        tk.Label(self.root, text="Choose Username:", font=("Arial", 12, "bold"), bg="#d0f0fd", fg="black").pack()
        username_entry = tk.Entry(self.root, font=("Arial", 12))
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Choose Password:", font=("Arial", 12, "bold"), bg="#d0f0fd", fg="black").pack()
        password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        password_entry.pack(pady=5)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            if username in users:
                messagebox.showwarning("Error", "Username already exists.")
            elif not username or not password:
                messagebox.showwarning("Error", "Please fill all fields.")
            else:
                users[username] = hash_password(password)
                save_user(username, password)
                messagebox.showinfo("Success", "Registration complete!")
                self.create_login_page()

        tk.Button(self.root, text="Register", font=("Arial", 12, "bold"), bg="#00bfff", fg="black", command=register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", font=("Arial", 10, "bold"), bg="#ccc", fg="black", command=self.create_login_page).pack()

    # --- Home Page After Login ---
    def create_home_page(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome, {self.username}", font=("Arial", 18, "bold"), bg="#d0f0fd", fg="black").pack(pady=30)

        tk.Button(self.root, text="Submit Feedback", font=("Arial", 14, "bold"), bg="#87ceeb", fg="black", width=20, command=self.student_page).pack(pady=10)
        tk.Button(self.root, text="View Feedback", font=("Arial", 14, "bold"), bg="#1e90ff", fg="black", width=20, command=self.admin_page).pack(pady=10)
        tk.Button(self.root, text="Logout", font=("Arial", 10, "bold"), bg="#ccc", fg="black", command=self.create_login_page).pack(pady=20)

    def student_page(self):
        self.clear_window()
        tk.Label(self.root, text="Submit Feedback", font=("Arial", 18, "bold"), bg="#d0f0fd", fg="black").pack(pady=20)

        tk.Label(self.root, text="Your Feedback:", font=("Arial", 12, "bold"), bg="#d0f0fd", fg="black").pack()
        feedback_text = tk.Text(self.root, height=5, width=50, font=("Arial", 12))
        feedback_text.pack(pady=5)

        def submit_feedback():
            feedback = feedback_text.get("1.0", tk.END).strip()
            if feedback:
                feedback_data.append((self.username, feedback))
                messagebox.showinfo("Success", "Feedback submitted!")
                self.create_home_page()
            else:
                messagebox.showwarning("Input Error", "Feedback cannot be empty.")

        tk.Button(self.root, text="Submit", font=("Arial", 12, "bold"), bg="#00bfff", fg="black", command=submit_feedback).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 10, "bold"), bg="#ccc", fg="black", command=self.create_home_page).pack()

    def admin_page(self):
        self.clear_window()
        tk.Label(self.root, text="View Feedback", font=("Arial", 18, "bold"), bg="#d0f0fd", fg="black").pack(pady=20)

        frame = tk.Frame(self.root, bg="#d0f0fd")
        frame.pack()

        columns = ("Name", "Feedback")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        tree.heading("Name", text="Student Name")
        tree.heading("Feedback", text="Feedback")
        tree.column("Name", width=150)
        tree.column("Feedback", width=400)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack()

        for entry in feedback_data:
            tree.insert('', tk.END, values=entry)

        tk.Button(self.root, text="Back", font=("Arial", 10, "bold"), bg="#ccc", fg="black", command=self.create_home_page).pack(pady=10)


# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FeedbackApp(root)
    root.mainloop()
