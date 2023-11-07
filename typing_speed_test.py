import tkinter as tk
import time
import random
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import webbrowser
import os
import datetime

class TypingSpeedTestApp:
    def __init__(self, master):
        self.master = master
        self.admin_logged_in = False
        self.admin_username = "admin"
        self.admin_password = "adminpass"
        self.connection = None
        self.users_tree = None
        self.logged_in = False
        self.username = ""
        self.password = ""
        self.timer_id = None  # Initialize the timer ID to None
        self.sentences = [
            "There was once a hare who was friends with a tortoise. One day, he challenged the tortoise to a race. Seeing how slow the tortoise was going, the hare thought he’ll win this easily. So he took a nap while the tortoise kept on going. When the hare woke up, he saw that the tortoise was already at the finish line. Much to his chagrin, the tortoise won the race while he was busy sleeping.",
            "Once there was a dog who wandered the streets night and day in search of food. One day, he found a big juicy bone and he immediately grabbed it between his mouth and took it home. On his way home, he crossed a river and saw another dog who also had a bone in its mouth. He wanted that bone for himself too. But as he opened his mouth, the bone he was biting fell into the river and sank. That night, he went home hungry.",
            "After flying a long distance, a thirsty crow was wandering the forest in search of water. Finally, he saw a pot half-filled with water. He tried to drink from it but his beak wasn’t long enough to reach the water inside. He then saw pebbles on the ground and one by one, he put them in the pot until the water rose to the brim. The crow then hastily drank from it and quenched his thirst.",
            "There was a boy named John who was so lazy, he couldn't even bother to change his clothes. One day, he saw that the apple tree in their yard was full of fruits. He wanted to eat some apples but he was too lazy to climb the tree and take the fruits. So he lay down underneath the tree and waited for the fruits to fall off. John waited and waited until he was very hungry but the apples never fell.",
            "Once there was a hungry fox who stumbled upon a vineyard. After seeing the round, juicy grapes hanging in a bunch, the fox drooled. But no matter how high he jumped, he couldn’t reach for it. So he told himself that it was probably sour and left. That night, he had to sleep on an empty stomach."
        ]

        self.sample_text = ""
        self.start_time = 0
        self.end_time = 0
        self.timer = None

        self.master.title("Typing Speed Test")
        self.master.attributes('-fullscreen', True)
        # Load the background image for the full screen
        background_image_fullscreen = Image.open("typing speed test/blue carbon background.jpg")
        resized_image_fullscreen = background_image_fullscreen.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.background_photo_fullscreen = ImageTk.PhotoImage(resized_image_fullscreen)

        # Create a label to display the blue carbon background image
        self.background_label = tk.Label(master, image=self.background_photo_fullscreen)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load the background image
        background_image = Image.open("typing speed test/background_image.jpg")  
        resized_image = background_image.resize((450, 200))  
        self.background_photo = ImageTk.PhotoImage(resized_image)

        # Create a canvas and place the background image
        self.canvas = tk.Canvas(master, width=450, height=200)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)
        self.canvas.pack()

        self.admin_frame = tk.Frame(master)
        self.admin_frame.pack()

        self.admin_ID_label = tk.Label(self.admin_frame, text="Admin ID:", font=("Arial", 14))
        self.admin_ID_label.pack(pady=10)

        self.admin_ID_entry = tk.Entry(self.admin_frame, width=50, font=("Arial", 12))
        self.admin_ID_entry.pack()

        self.admin_PW_label = tk.Label(self.admin_frame, text="Admin Password:", font=("Arial", 14))
        self.admin_PW_label.pack(pady=10)

        self.admin_PW_entry = tk.Entry(self.admin_frame, show="*", width=50, font=("Arial", 12))
        self.admin_PW_entry.pack()

        self.admin_login_button = tk.Button(self.admin_frame, text="Login as Admin", command=self.admin_login, font=("Arial", 12))
        self.admin_login_button.pack(pady=10)
        
        self.user_login_button = tk.Button(self.admin_frame, text="User Login", command=self.show_user_login, font=("Arial", 12))
        self.user_login_button.pack(pady=10)

        self.view_all_users_button = tk.Button(self.admin_frame, text="View All Users", command=self.view_all_users, font=("Arial", 12))
        self.view_all_users_button.pack(pady=10)

        self.admin_logout_button = tk.Button(self.admin_frame, text="logout as admin", command=self.logout_as_admin, font=("Arial", 12))
        self.admin_logout_button.pack(pady=10)

        self.users_tree = ttk.Treeview(self.admin_frame, columns=("ID", "Username", "Email", "Role"))
        self.users_tree.heading("#1", text="ID")
        self.users_tree.heading("#2", text="Username")
        self.users_tree.heading("#3", text="Email")
        self.users_tree.heading("#4", text="Role")
                
        self.login_frame = tk.Frame(master)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Arial", 14))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self.login_frame, width=50, font=("Arial", 12))
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Arial", 14))
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.login_frame, show="*", width=50, font=("Arial", 12))
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.user_login, font=("Arial", 12))
        self.login_button.pack(pady=10)

        self.admin_login_button1 = tk.Button(self.login_frame, text="Admin Login", command=self.show_admin_login, font=("Arial", 12))
        self.admin_login_button1.pack(pady=10)

        self.register_frame = tk.Frame(master)
        self.register_frame.pack()

        self.register_first_name_label = tk.Label(self.register_frame, text="First Name:", font=("Arial", 14))
        self.register_first_name_label.pack(pady=10)

        self.register_first_name_entry = tk.Entry(self.register_frame, width=50, font=("Arial", 12))
        self.register_first_name_entry.pack()

        self.register_last_name_label = tk.Label(self.register_frame, text="Last Name:", font=("Arial", 14))
        self.register_last_name_label.pack(pady=10)

        self.register_last_name_entry = tk.Entry(self.register_frame, width=50, font=("Arial", 12))
        self.register_last_name_entry.pack()

        self.register_email_label = tk.Label(self.register_frame, text="Email Id:", font=("Arial", 14))
        self.register_email_label.pack(pady=10)

        self.register_email_entry = tk.Entry(self.register_frame, width=50, font=("Arial", 12))
        self.register_email_entry.pack()

        self.register_username_label = tk.Label(self.register_frame, text="Username:", font=("Arial", 14))
        self.register_username_label.pack(pady=10)

        self.register_username_entry = tk.Entry(self.register_frame, width=50, font=("Arial", 12))
        self.register_username_entry.pack()

        self.register_password_label = tk.Label(self.register_frame, text="Set Password:", font=("Arial", 14))
        self.register_password_label.pack(pady=10)

        self.register_password_entry = tk.Entry(self.register_frame, show="*", width=50, font=("Arial", 12))
        self.register_password_entry.pack()

        self.register_button = tk.Button(self.register_frame, text="Register", command=self.register_user, font=("Arial", 12))
        self.register_button.pack(pady=10)

        self.login_register_button = tk.Button(self.login_frame, text="Register", command=self.show_register_frame, font=("Arial", 12))
        self.login_register_button.pack(pady=10)
        
        self.exit_button = tk.Button(self.login_frame, text="Exit", command=master.quit, font=("Arial", 12))
        self.exit_button.pack(pady=10)

        self.exit_button = tk.Button(self.register_frame, text="Exit", command=master.quit, font=("Arial", 12))
        self.exit_button.pack(pady=10)

        self.exit_button = tk.Button(self.admin_frame, text="Exit", command=master.quit, font=("Arial", 12))
        self.exit_button.pack(pady=10)

        self.register_frame.pack_forget()  # Hide the register frame initially
        self.admin_frame.pack_forget()     # Hide the admin frame initially
        self.view_all_users_button.pack_forget()
        self.admin_logout_button.pack_forget()

        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        # Create admin menu options
        self.admin_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Admin", menu=self.admin_menu)

        self.admin_menu.add_command(label="View All Users", command=self.view_all_users)
        self.admin_menu.add_command(label="Logout as Admin", command=self.logout_as_admin, state=tk.DISABLED)

        # Hide admin menu options initially
        self.admin_menu.entryconfig("View All Users", state=tk.DISABLED)

        self.connection = sqlite3.connect('typing_speed_test.db')
        self.create_table()        

        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="Reset", command=self.reset)
        self.file_menu.add_command(label="Exit", command=master.quit)

        self.name_time_selection_frame = None  # Initialize name_time_selection_frame to None

        self.name_time_selection_frame = None
        self.typing_test_frame = None

    def admin_login(self):
        admin_username = self.admin_ID_entry.get()
        admin_password = self.admin_PW_entry.get()

        if admin_username == self.admin_username and admin_password == self.admin_password:
            # Correct admin credentials, grant access to admin controls
            self.admin_logged_in = True
            self.admin_ID_entry.config(state=tk.DISABLED)
            self.admin_PW_entry.config(state=tk.DISABLED)
            self.admin_login_button.config(state=tk.DISABLED)

            # Hide the admin login button
            self.admin_login_button.pack_forget()

            # Show the admin buttons
            self.view_all_users_button.pack()
            self.admin_logout_button.pack()

            self.admin_menu.entryconfig("View All Users", state=tk.NORMAL)
            self.admin_menu.entryconfig("Logout as Admin", state=tk.NORMAL)

            messagebox.showinfo("Admin Login Successful", "You are logged in as Admin.")
        else:
            messagebox.showerror("Admin Login Failed", "Incorrect admin username or password.")

    def view_all_users(self):
        # Fetch all user information from the database
        query = "SELECT * FROM user_info"
        cursor = self.connection.cursor()
        cursor.execute(query)
        all_users = cursor.fetchall()
        cursor.close()

        if not all_users:
            # If there are no users, show a message
            messagebox.showinfo("View All Users", "No users found.")
        else:
            # Create a new window to display user details
            users_window = tk.Toplevel(self.master)
            users_window.title("All Users")

            # Create a canvas for scrolling
            canvas = tk.Canvas(users_window)
            canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            # Create a scrollbar and associate it with the canvas
            scrollbar = tk.Scrollbar(users_window, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame to contain the user details
            users_frame = tk.Frame(users_window)
            users_frame.pack(padx=20, pady=20)

            # Header labels
            headers = ["User ID", "First Name", "Last Name", "Email", "Username", "Password"]
            for col, header in enumerate(headers):
                header_label = tk.Label(users_frame, text=header, font=("Arial", 12, "bold"))
                header_label.grid(row=0, column=col, padx=5, pady=5)

            # User data
            for row, user in enumerate(all_users, start=1):
                for col, data in enumerate(user):
                    user_label = tk.Label(users_frame, text=data, font=("Arial", 12))
                    user_label.grid(row=row, column=col, padx=5, pady=5)

                # Add Edit and Delete buttons for each user row
                edit_button = tk.Button(users_frame, text="Edit", command=lambda user_id=user[0]: self.edit_user_details(user_id))
                edit_button.grid(row=row, column=len(headers), padx=5, pady=5)

                delete_button = tk.Button(users_frame, text="Delete", command=lambda user=user: self.delete_user(user[0]))
                delete_button.grid(row=row, column=len(headers)+1, padx=5, pady=5)

            # Configure canvas scrolling region
            users_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

            # Bind canvas scrolling to mousewheel
            canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

            # Adjust the window size based on the number of users
            window_width = 800
            window_height = min(600, (row+1) * 50)
            users_window.geometry(f"{window_width}x{window_height}")

    def edit_user_details(self, user_id):
        # Fetch user information from the database based on user_id
        query = "SELECT * FROM user_info WHERE UserID = ?"
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        user_info = cursor.fetchone()
        cursor.close()

        if user_info:
            self.show_edit_user_window(user_info)
        else:
            messagebox.showerror("Error", "User information not found.")

    def show_edit_user_window(self, user_info):
        user_id, first_name, last_name, email, username, password = user_info

        # Create a new window to edit user details
        edit_user_window = tk.Toplevel(self.master)
        edit_user_window.title("Edit User Details")

        # Create a frame to contain the user details form
        edit_user_frame = tk.Frame(edit_user_window)
        edit_user_frame.pack(padx=10, pady=10)

        # Editable fields
        first_name_label = tk.Label(edit_user_frame, text="First Name:", font=("Arial", 14))
        first_name_label.pack(anchor="w", padx=10, pady=10)
        first_name_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        first_name_entry.pack(fill="x", padx=10, pady=10)
        first_name_entry.insert(tk.END, first_name)

        last_name_label = tk.Label(edit_user_frame, text="Last Name:", font=("Arial", 14))
        last_name_label.pack(anchor="w", padx=10, pady=10)
        last_name_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        last_name_entry.pack(fill="x", padx=10, pady=10)
        last_name_entry.insert(tk.END, last_name)

        email_label = tk.Label(edit_user_frame, text="Email Id:", font=("Arial", 14))
        email_label.pack(anchor="w", padx=10, pady=10)
        email_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        email_entry.pack(fill="x", padx=10, pady=10)
        email_entry.insert(tk.END, email)

        # Disable editing of the username field
        username_label = tk.Label(edit_user_frame, text="Username:", font=("Arial", 14))
        username_label.pack(anchor="w", padx=10, pady=10)
        username_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        username_entry.pack(fill="x", padx=10, pady=10)
        username_entry.insert(tk.END, username)

        password_label = tk.Label(edit_user_frame, text="Set Password:", font=("Arial", 14))
        password_label.pack(anchor="w", padx=10, pady=10)
        password_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        password_entry.pack(fill="x", padx=10, pady=10)
        password_entry.insert(tk.END, password)

        # Label and Entry pairs for each attribute
        attribute_labels = ["First Name", "Last Name", "Email", "Username", "Set Password"]
        attribute_entries = [first_name, last_name, email, username, password]

        for label_text, entry_text in zip(attribute_labels, attribute_entries):
            label = tk.Label(edit_user_frame, text=f"{label_text}:", font=("Arial", 14))
            label.pack(anchor="w", padx=10, pady=10)
            entry = tk.Entry(edit_user_frame, font=("Arial", 12))
            entry.pack(fill="x", padx=10, pady=10)
            entry.insert(tk.END, entry_text)
            break
        # Save button to update the user details
        save_button = tk.Button(edit_user_frame, text="Save Changes", command=lambda: self.update_user(user_id, attribute_entries[0].get(), attribute_entries[1].get(), attribute_entries[2].get(), attribute_entries[4].get()))
        save_button.pack(side="right", padx=10, pady=10)

    def update_user(self, user_id, first_name, last_name, email, username, password):
        query = "UPDATE user_info SET FirstName=?, LastName=?, Email=?, Username=?, Password=? WHERE UserID=?"
        query1 = "UPDATE users SET Username=?, Password=? WHERE UserID=?"
        cursor = self.connection.cursor()
        cursor.execute(query, (first_name, last_name, email, username, password, user_id))
        cursor.execute(query1, (username, password, user_id))
        self.connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "User details updated successfully.")
        # Refresh the view_all_users window to reflect the updated details
        self.view_all_users()

    def delete_user(self, user_id):
        result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
        if result:
            query = "DELETE FROM user_info WHERE UserID=?"
            query1 = "DELETE FROM users WHERE UserID=?"
            cursor = self.connection.cursor()
            cursor.execute(query, (user_id,))
            cursor.execute(query1, (user_id,))
            self.connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "User deleted successfully.")
            # Refresh the view_all_users window to reflect the updated list
            self.view_all_users()

    def logout_as_admin(self):
        self.admin_logged_in = False
        self.admin_ID_entry.config(state=tk.NORMAL)  # Fix this line
        self.admin_PW_entry.config(state=tk.NORMAL)  # Fix this line
        self.admin_login_button.config(state=tk.NORMAL)

        self.view_all_users_button.pack_forget()
        self.admin_logout_button.pack_forget()
        self.admin_login_button.pack()

        self.admin_menu.entryconfig("View All Users", state=tk.DISABLED)
        self.admin_menu.entryconfig("Logout as Admin", state=tk.DISABLED)

        # Optionally, clear admin login fields if needed
        self.admin_ID_entry.delete(0, tk.END)
        self.admin_PW_entry.delete(0, tk.END)

        messagebox.showinfo("Admin Logout", "You are logged out as Admin.")

    def show_admin_login(self):
        # Hide the login frame and show the admin login frame
        self.login_frame.pack_forget()
        self.admin_frame.pack()
        
        self.admin_ID_entry.delete(0, tk.END)
        self.admin_PW_entry.delete(0, tk.END)
        # Optionally, clear user login fields if needed
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END) 

    def show_user_login(self):
        # Hide the admin login frame and show the user login frame
        self.admin_frame.pack_forget()
        self.login_frame.pack()

        # Optionally, clear admin login fields if needed
        self.admin_ID_entry.delete(0, tk.END)
        self.admin_PW_entry.delete(0, tk.END)
        # Optionally, clear user login fields if needed
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


    def create_table(self):

        cursor = self.connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(255),
            Password VARCHAR(255)
        );
        ''')
        
        # Create a table for user information if it does not exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName VARCHAR(255),
            LastName VARCHAR(255),
            Email VARCHAR(255),
            Username VARCHAR(255),
            Password VARCHAR(255)
        );
        ''')

        # Create a table for scores if it does not exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            Username VARCHAR(255),
            Name VARCHAR(255),
            speed VARCHAR(255),
            accuracy VARCHAR(255)
        );
        ''')

        self.connection.commit()

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()

    def register_user(self):
        username = self.register_username_entry.get()
        first_name = self.register_first_name_entry.get()
        last_name = self.register_last_name_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()

        if username and first_name and last_name and email and password:
            # Store the user credentials in the database
            query = "INSERT INTO users (Username, Password) VALUES (?, ?)"
            query_info = "INSERT INTO user_info (FirstName, LastName, Email, Username, Password) VALUES (?, ?, ?, ?, ?)"
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, (username, password))
                cursor.execute(query_info, (first_name, last_name, email, username, password))
                self.connection.commit()
                cursor.close()
                messagebox.showinfo("Sucess!!!","Registered new user successfully!!!")
                # Hide the register frame and show the login frame again
                self.register_frame.pack_forget()
                self.login_frame.pack()
                self.register_username_entry.delete(0, tk.END)
                self.register_first_name_entry.delete(0, tk.END)
                self.register_last_name_entry.delete(0, tk.END)
                self.register_email_entry.delete(0, tk.END)
                self.register_password_entry.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Attention!!!","User already exists with this username.")
        else:
            messagebox.showwarning("Attention!!!","Please fill in all the fields.")

    def user_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            # Check if the provided username and password exist in the database
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            
            # Create a cursor object from the connection
            cursor = self.connection.cursor()
            # Execute the query using the cursor
            cursor.execute(query, (username, password))
            user_data = cursor.fetchone()
            cursor.close()  # Close the cursor after using it

            if user_data:
                # Correct username and password, proceed to typing test
                self.logged_in = True
                self.username = username
                self.password = password
                self.login_frame.pack_forget()
                self.show_name_and_time_selection()
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                messagebox.showinfo("Success Message!!!", "Login Successful!!!.")
            else:
                # Incorrect username or password
                messagebox.showerror("Attention!!!", "Incorrect username or password")
        else:
            messagebox.showwarning("Attention!!!", "Please enter both username and password.")


    def show_name_and_time_selection(self):
        if self.logged_in:
            if self.name_time_selection_frame is not None:
                self.name_time_selection_frame.pack_forget()

            self.name_time_selection_frame = tk.Frame(self.master)
            self.name_time_selection_frame.pack()

            self.name_label = tk.Label(self.name_time_selection_frame, text="Enter your name:", font=("Arial", 14))
            self.name_label.pack(pady=10)

            self.name_entry = tk.Entry(self.name_time_selection_frame, width=50, font=("Arial", 12))
            self.name_entry.pack()

            self.time_label = tk.Label(self.name_time_selection_frame, text="Select the Time Frame (in seconds):", font=("Arial", 14))
            self.time_label.pack(pady=10)

            self.selected_time = tk.IntVar()
            self.time_spinbox = tk.Spinbox(self.name_time_selection_frame, from_=60, to=300, increment=120, textvariable=self.selected_time, font=("Arial", 12))
            self.time_spinbox.pack()

            self.next_button = tk.Button(self.name_time_selection_frame, text="Next", command=self.show_typing_test, font=("Arial", 12))
            self.next_button.pack(pady=10)

            self.name_label.pack_forget

        # Create the info frame with article and video links
        self.info_frame = tk.Frame(self.name_time_selection_frame, bg="white")
        self.info_frame.pack(pady=15)

        self.article_label = tk.Label(self.info_frame, text=" Please find the below Article and utilze it well\nImprove your Typing Skill", font=("Arial", 12))
        self.article_label.pack(pady=5)

        self.article_button = tk.Button(self.info_frame, text="Open Typing Test Article", command=self.open_typing_test_article, font=("Arial", 12))
        self.article_button.pack(pady=5)

        self.video_button = tk.Button(self.info_frame, text="Open Typing Test Video", command=self.open_typing_test_video, font=("Arial", 12))
        self.video_button.pack(pady=5)

    def start_typing_test(self, duration_seconds):
        self.sample_text = random.choice(self.sentences)
        self.text_label = tk.Label(self.typing_test_frame, text=self.sample_text, wraplength=500, font=("Arial", 14))
        self.text_label.pack(pady=20)

        self.entry = tk.Entry(self.typing_test_frame, width=50, font=("Arial", 12))
        self.entry.pack()

        # Display the current login time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.login_time_label = tk.Label(self.typing_test_frame, text=f"Logged-in at: {current_time}", font=("Arial", 12))
        self.login_time_label.pack(pady=10)

        self.result_label = tk.Label(self.typing_test_frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def start_typing(self, duration_seconds):
        self.start_time = time.time()
        self.end_time = self.start_time + duration_seconds

        self.start_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.entry.bind("<Return>", self.end_typing)

        self.timer_id = self.master.after(1000, self.update_timer)

    def end_typing(self, event):
        # Cancel the timer using self.timer_id
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.master.after_cancel(self.timer)
        self.end_time = time.time()
        self.entry.config(state=tk.DISABLED)
        self.calculate_results()
        self.save_results()

    def update_timer(self):
        current_time = time.time()
        remaining_time = self.end_time - current_time

        if remaining_time <= 0:
            remaining_time = 0
            self.end_typing(None)

        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = f"Time Remaining: {minutes:02d}:{seconds:02d}"
        display_text = f"{timer_text}\n\n{self.sample_text}"
        self.text_label.config(text=display_text)

        if remaining_time <= 0:
            self.master.after_cancel(self.timer)
        else:
            self.timer = self.master.after(1000, self.update_timer)

    def calculate_results(self):
        user_text = self.entry.get()
        total_time = self.end_time - self.start_time
        words_typed = len(user_text.split())
        wpm = int(words_typed / (total_time / 60))
        accuracy = self.calculate_accuracy(user_text)

        self.results = {
            "Name": self.name,
            "Words per minute": wpm,
            "Accuracy": accuracy
        }

        result_text = f"Words per minute: {wpm}\nAccuracy: {accuracy}%"
        self.result_label.config(text=result_text)

        self.start_button.config(state=tk.NORMAL)

    def calculate_accuracy(self, user_text):
        correct_chars = sum(user_char == sample_char for user_char, sample_char in zip(user_text, self.sample_text))
        total_chars = max(len(user_text), len(self.sample_text))
        accuracy = int((correct_chars / total_chars) * 100)
        return accuracy

    def save_results(self):
        if self.logged_in:
            Username = self.username  # Assuming you've stored the username during login
            wpm = self.results["Words per minute"]
            accuracy = self.results["Accuracy"]
            Name= self.name
            # Insert the results into the database
            query = "INSERT INTO scores (Username, Name, speed, accuracy) VALUES (?, ?, ?, ?)"
            cursor = self.connection.cursor()
            cursor.execute(query, (Username, Name, wpm, accuracy))
            self.connection.commit()
            cursor.close()
            messagebox.showinfo("Success Message", "Results saved successfully!")
        
        else:
            messagebox.showwarning("Attention!!!", "You need to log in before saving results.")

    def show_previous_results(self):
        if self.logged_in:
            previous_results_window = tk.Toplevel(self.master)
            previous_results_window.title("Previous Results")

            # Fetch previous results for the currently logged-in user from the database
            query = "SELECT Name, speed, accuracy FROM scores WHERE Username = ?"
            cursor = self.connection.cursor()
            cursor.execute(query, (self.username,))
            results = cursor.fetchall()
            cursor.close()

            if len(results) == 0:
                no_results_label = tk.Label(previous_results_window, text="No previous results found.", font=("Arial", 12))
                no_results_label.pack(pady=10)
            else:
                results_table = tk.Label(previous_results_window, text="Previous Results", font=("Arial", 14, "bold"))
                results_table.pack()

                header_frame = tk.Frame(previous_results_window)
                header_frame.pack()

                name_label = tk.Label(header_frame, text="Name", font=("Arial", 12, "bold"), padx=10)
                name_label.pack(side=tk.LEFT)

                wpm_label = tk.Label(header_frame, text="Words per Minute", font=("Arial", 12, "bold"), padx=10)
                wpm_label.pack(side=tk.LEFT)

                accuracy_label = tk.Label(header_frame, text="Accuracy", font=("Arial", 12, "bold"), padx=10)
                accuracy_label.pack(side=tk.LEFT)

                for result in results:
                    result_frame = tk.Frame(previous_results_window)
                    result_frame.pack()

                    name = result[0]  # Name
                    wpm = result[1]   # Words per minute
                    accuracy = result[2]  # Accuracy

                    name_label = tk.Label(result_frame, text=name, font=("Arial", 12), padx=10)
                    name_label.pack(side=tk.LEFT)

                    wpm_label = tk.Label(result_frame, text=wpm, font=("Arial", 12), padx=10)
                    wpm_label.pack(side=tk.LEFT)

                    accuracy_label = tk.Label(result_frame, text=accuracy, font=("Arial", 12), padx=10)
                    accuracy_label.pack(side=tk.LEFT)
        else:
            messagebox.showwarning("Attention!!!", "You need to log in to view previous results.")


    def reset(self):
        self.name_entry.delete(0, tk.END)
        self.name_entry.config(state=tk.NORMAL)
        self.name_label.config(text="Enter your name:")
        self.name_label.pack_forget()
        self.time_label.pack(pady=10)
        self.time_spinbox.pack()
        self.next_button.pack(pady=10)
        self.typing_test_frame.pack_forget()
        self.name_time_selection_frame.pack()

    def show_typing_test(self):
        if self.name_time_selection_frame is not None:
            self.name_time_selection_frame.pack_forget()

        self.name = self.name_entry.get()
        self.name_label = tk.Label(text=f"Welcome, {self.name}!",font=("Arial", 18, "bold"), fg="blue")
        self.name_label.pack(pady=20)

        self.typing_test_frame = tk.Frame(self.master)
        self.typing_test_frame.pack()

        self.time_label.pack_forget()
        self.time_spinbox.pack_forget()
        self.next_button.pack_forget()

        duration_seconds = self.selected_time.get()
        self.start_typing_test(duration_seconds)

        self.start_time = 0
        self.end_time = 0
        self.timer = None

        # Create the button frame for start, logout, show results, and reset buttons
        button_frame = tk.Frame(self.typing_test_frame)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame,text="Start",command=lambda: self.start_typing(duration_seconds),font=("Arial", 12))
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.logout_button = tk.Button(button_frame,text="Logout",command=self.logout,font=("Arial", 12))
        self.logout_button.pack(side=tk.LEFT, padx=5)

        self.show_results_button = tk.Button(button_frame,text="Show Previous Results",command=self.show_previous_results,font=("Arial", 12))
        self.show_results_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame,text="Reset",command=self.reset,font=("Arial", 12))
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.exit_button_typing_test = tk.Button(button_frame,text="Exit",command=self.exit_typing_test,font=("Arial", 12))
        self.exit_button_typing_test.pack(side=tk.LEFT, padx=5)
        # Add the info_frame to the typing_test_frame
        self.info_frame.pack(side=tk.BOTTOM, pady=10)

    def exit_typing_test(self):
        # Call master.quit() to close the application
        self.master.quit()

    # def __del__(self):
    #     # Close the connection to the database when the object is deleted
    #     self.connection.close()

    def logout(self):
        self.name_entry.delete(0, tk.END)
        self.name_entry.config(state=tk.NORMAL)
        self.name_label.config(text="Enter your name:")
        self.name_label.pack_forget()
        self.time_label.pack(pady=10)
        self.time_spinbox.pack()
        self.next_button.pack(pady=10)
        self.logged_in = False
        self.typing_test_frame.pack_forget()
        self.name_time_selection_frame.pack_forget()
        # Show the login frame again
        self.login_frame.pack()

    def open_typing_test_video(self):
        video_url = "https://www.youtube.com/watch?v=tuWFNrfjy-c"  
        webbrowser.open(video_url)

    def open_typing_test_article(self):
        article_file_path = r"C:\Users\Logeshkumar\Desktop\Python\Touch Typing Lessons.pdf"  
        if os.path.exists(article_file_path):
            os.startfile(article_file_path)
        else:
            messagebox.showerror("Attention!!!","Article file not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()
