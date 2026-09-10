import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter.font import Font
import mysql.connector
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

class StoryWriterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WordWeaver")
        self.root.geometry("800x600")
        self.root.configure(bg='lightblue')
        self.custom_font = Font(family="Cinzel", size=20, weight="bold")
        self.phrase_font = Font(family="Times New Roman", size=12)
        self.user_inputs = {} # Dictionary to store user inputs
        self.username = None  # Will hold the username once logged in or registered
        self.setup_database()
        self.load_gpt_model() # Initialize GPT-2 model
        self.show_login_screen()

        if self.username:
            self.create_widgets()


    def setup_database(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="wordweaver"
        )
        self.cursor = self.db.cursor()

        #table to store user inputs
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stories (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            characters TEXT,
            setting TEXT,
            content TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL 
        )''')
        self.db.commit()

    def load_gpt_model(self):
        # Load GPT-2 model and tokenizer from HuggingFace
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")

    def show_login_screen(self):
        """Display the login or registration screen."""
        self.login_screen = tk.Toplevel(self.root)
        self.login_screen.title("Login or Register")
        self.login_screen.geometry("400x300")
        self.login_screen.configure(bg='white')
        self.login_screen.protocol("WM_DELETE_WINDOW", self.root.quit)  # Close main window if login is closed

        # Frame for the login form
        form_frame = tk.Frame(self.login_screen, bg='white')
        form_frame.pack(expand=True, padx=20, pady=20)

        # Username label and entry
        tk.Label(form_frame, text="Username", bg='white', font=("Arial", 12)).pack(pady=(10, 5))
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        # Password label and entry
        tk.Label(form_frame, text="Password", bg='white', font=("Arial", 12)).pack(pady=(10, 5))
        self.password_entry = tk.Entry(form_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        # Login and Register buttons
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(pady=(20, 10))
        
        login_button = tk.Button(buttons_frame, text="Login", command=self.login_user, font=("Arial", 12), bg='lightblue')
        login_button.pack(side=tk.LEFT, padx=10)
        
        register_button = tk.Button(buttons_frame, text="Register", command=self.register_user, font=("Arial", 12), bg='lightblue')
        register_button.pack(side=tk.LEFT, padx=10)

    def login_user(self):
        """Handle user login."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Fetch user record from the database
        self.cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
        result = self.cursor.fetchone()

        # Check if the password matches
        if result and password == result[0]:  # Compare plaintext passwords
            self.username = username
            messagebox.showinfo("Login Successful", f"Welcome back, {self.username}!")
            self.login_screen.destroy()  # Close the login screen
            self.create_widgets()  # Set up main window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register_user(self):
        """Handle user registration."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username already exists
        self.cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
        if self.cursor.fetchone()[0] > 0:
            messagebox.showwarning("Username Taken", "This username is already taken. Please choose another.")
        else:
            # Store the plaintext password directly
            self.cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            self.db.commit()
            self.username = username
            messagebox.showinfo("Registration Successful", f"Account created successfully, {self.username}!")
            self.login_screen.destroy()  # Close the login screen
            self.create_widgets()  # Set up main window


    def create_widgets(self):
        #name
        self.title_label = tk.Label(self.root,
                                    text="Story Writer",
                                    font=self.custom_font,
                                    bg='lightblue')
        self.title_label.pack(pady=20)

        self.phrase_label = tk.Label(self.root,
                                     text="Unleash your creativity with ease!",
                                     font=self.phrase_font,
                                     bg='lightblue')
        self.phrase_label.pack(pady=5)

        #start
        self.get_started_button = tk.Button(self.root,
                                            text="Get Started",
                                            command=self.show_options,
                                            bg='white')
        self.get_started_button.pack(pady=20)

        #exist
        self.existing_button = tk.Button(self.root,
                                         text="Existing Stories",
                                         command=self.show_existing_stories,
                                         bg='white')
        self.existing_button.pack(pady=10)

        #used data
        self.my_stories_button = tk.Button(self.root,
                                           text="My Stories",
                                           command=self.show_my_stories,
                                           bg='white')
        self.my_stories_button.pack(pady=10)

        #logout
        logout_button = tk.Button(self.root, text="Logout", command=self.logout, bg='red', fg='white')
        logout_button.pack(side=tk.TOP, pady=10)

    def logout(self):
        # Close the current main screen
        self.root.destroy()
        
        # Reset any user session data if needed
        self.username = None
        self.user_inputs = {
            'genre': None,
            'character': None,
            'setting': None,
            'length': None,
            'extras': None
        }
        
        # Reinitialize the root for the login_or_register page
        self.root = tk.Tk()

        # Call the login_or_register method to display the login/register page again
        self.show_login_screen()
        self.root.mainloop()

    def show_options(self):
        self.title_label.pack_forget()
        self.phrase_label.pack_forget()
        self.get_started_button.pack_forget()
        self.existing_button.pack_forget()
        self.my_stories_button.pack_forget()

        self.title_label.pack(pady=5)
        self.phrase_label.pack(pady=2)

        #options
        self.genre_button = tk.Button(self.root,
                                      text="Genre",
                                      command=self.choose_genre,
                                      bg='white')
        self.genre_button.place(x=140, y=140, width=200, height=50)

        self.character_button = tk.Button(self.root,
                                          text="Character",
                                          command=self.choose_characters,
                                          bg='white')
        self.character_button.place(x=140, y=200, width=200, height=50)

        self.setting_button = tk.Button(self.root,
                                        text="Setting",
                                        command=self.choose_setting,
                                        bg='white')
        self.setting_button.place(x=290, y=260, width=200, height=50)

        self.length_button = tk.Button(self.root,
                                       text="No. of Words",
                                       command=self.choose_length,
                                       bg='white')
        self.length_button.place(x=440, y=200, width=200, height=50)

        self.extras_button = tk.Button(self.root,
                                       text="Extras",
                                       command=self.choose_extras,
                                       bg='white')
        self.extras_button.place(x=440, y=140, width=200, height=50)

        #submit
        self.submit_button = tk.Button(self.root,
                                       text="Submit",
                                       command=self.generate_story,
                                       bg='white',
                                       state=tk.DISABLED)
        self.submit_button.place(x=300, y=500, width=200, height=50)

        #back
        self.back_button = tk.Button(self.root,
                                     text="Back",
                                     command=self.go_back,
                                     bg='white')
        self.back_button.place(x=300, y=550, width=200, height=50)

        self.user_inputs = {
            'genre': None,
            'character': None,
            'setting': None,
            'length': None,
            'extras': None
        }

    def go_back(self):
        self.genre_button.place_forget()
        self.character_button.place_forget()
        self.setting_button.place_forget()
        self.length_button.place_forget()
        self.extras_button.place_forget()
        self.submit_button.place_forget()
        self.back_button.place_forget()

        self.title_label.pack(pady=20)
        self.phrase_label.pack(pady=5)
        self.get_started_button.pack(pady=20)
        self.existing_button.pack(pady=10)
        self.my_stories_button.pack(pady=10)

    def choose_genre(self):
        genre_window = tk.Toplevel(self.root)
        genre_window.title("Choose Genre")
        genre_window.geometry("400x300")
        genre_window.configure(bg='lightblue')

        genres = ["Fantasy", "Science Fiction", "Mystery", "Romance", "Thriller", "Horror", "Other"]

        self.selected_genres = []

        def on_genre_select(genre):
            if genre == "Other":
                other_genre = simpledialog.askstring("Other Genre", "Please specify:")
                if other_genre:
                    self.selected_genres.append(other_genre)
            else:
                self.selected_genres.append(genre)
           
            messagebox.showinfo("Genre Selected", f"You selected: {', '.join(self.selected_genres)}")
            genre_window.destroy()
            self.user_inputs['genre'] = self.selected_genres
            self.check_submit_availability()

        for genre in genres:
            genre_button = tk.Button(genre_window, text=genre, command=lambda g=genre: on_genre_select(g), bg='white')
            genre_button.pack(pady=5)

        genre_window.mainloop()

    def choose_characters(self):
        character_window = tk.Toplevel(self.root)
        character_window.title("Choose Main Characters")
        character_window.geometry("400x400")
        character_window.configure(bg='lightblue')

        self.characters = []  # Reset the character list for each new story

        def add_character_fields(num_characters):
            # Clear any existing fields
            for widget in character_window.winfo_children():
                widget.destroy()
                
            tk.Label(character_window, text="Enter details for each character", bg='lightblue').pack(pady=10)

            # Dynamically create entry fields for each character
            for i in range(num_characters):
                tk.Label(character_window, text=f"Character {i + 1} Name:", bg='lightblue').pack(pady=5)
                name_entry = tk.Entry(character_window)
                name_entry.pack(pady=5)

                tk.Label(character_window, text=f"Character {i + 1} Personality:", bg='lightblue').pack(pady=5)
                personality_entry = tk.Entry(character_window)
                personality_entry.pack(pady=5)

                tk.Label(character_window, text=f"Character {i + 1} Role (Optional):", bg='lightblue').pack(pady=5)
                role_entry = tk.Entry(character_window)
                role_entry.pack(pady=5)

                self.characters.append({
                    'name_entry': name_entry,
                    'personality_entry': personality_entry,
                    'role_entry': role_entry
                })

            # Confirm button to save characters
            confirm_button = tk.Button(character_window, text="Save Characters", command=save_characters, bg='white')
            confirm_button.pack(pady=20)

        def set_num_characters():
            num_characters = simpledialog.askinteger("Number of Main Characters", "Enter the number of main characters:")
            if num_characters:
                add_character_fields(num_characters)

        def save_characters():
            # Extract input data and store it
            main_characters = []
            for character_entries in self.characters:
                name = character_entries['name_entry'].get()
                personality = character_entries['personality_entry'].get()
                role = character_entries['role_entry'].get()

                # Collect main character data if name and personality are provided
                if name and personality:
                    main_characters.append({
                        'name': name,
                        'personality': personality,
                        'role': role if role else "No specific role"
                    })

            # Save main characters into user_inputs dictionary
            if main_characters:
                self.user_inputs['character'] = main_characters
                messagebox.showinfo("Characters Set", f"{len(main_characters)} main character(s) have been saved.")
                character_window.destroy()
                self.check_submit_availability()
            else:
                messagebox.showwarning("Incomplete Data", "Please provide name and personality for each character.")

        # Button to start setting character fields based on number of main characters
        set_button = tk.Button(character_window, text="Set Number of Main Characters", command=set_num_characters, bg='white')
        set_button.pack(pady=20)

        character_window.mainloop()

        
    def choose_setting(self):
        setting_window = tk.Toplevel(self.root)
        setting_window.title("Choose Setting")
        setting_window.geometry("400x300")
        setting_window.configure(bg='lightblue')

        self.setting = None

        def set_setting():
            setting = simpledialog.askstring("Setting", "Enter the story setting:")
            if setting:
                self.setting = setting
                messagebox.showinfo("Setting Selected", f"Setting: {self.setting}")
                setting_window.destroy()
                self.user_inputs['setting'] = self.setting
                self.check_submit_availability()

        set_button = tk.Button(setting_window, text="Set Setting", command=set_setting, bg='white')
        set_button.pack(pady=20)

        setting_window.mainloop()

    def choose_length(self):
        length_window = tk.Toplevel(self.root)
        length_window.title("Choose Length")
        length_window.geometry("400x300")
        length_window.configure(bg='lightblue')

        self.length = None

        def set_length():
            length = simpledialog.askinteger("Length", "Enter the number of words:")
            if length:
                self.length = length
                messagebox.showinfo("Length Set", f"Story length: {self.length} words")
                length_window.destroy()
                self.user_inputs['length'] = self.length
                self.check_submit_availability()

        set_button = tk.Button(length_window, text="Set Length", command=set_length, bg='white')
        set_button.pack(pady=20)

        length_window.mainloop()

    def show_existing_stories(self):
        existing_window = tk.Toplevel(self.root)
        existing_window.title("Existing Stories")
        existing_window.geometry("400x400")
        existing_window.configure(bg='lightblue')

        # Define the path to the main folder where genre files are stored
        genre_folder_path = r"D:\wordweaved"

        # Create the folder if it doesn't exist yet (e.g. on first run) so this
        # doesn't crash with FileNotFoundError before any story has been generated
        os.makedirs(genre_folder_path, exist_ok=True)

        # Get all genre files in the folder
        genre_files = [f for f in os.listdir(genre_folder_path) if f.endswith('_stories.txt')]

        # Function to display stories within a genre file
        def display_genre_stories(filename):
            with open(os.path.join(genre_folder_path, filename), 'r') as file:
                stories = file.read()
            messagebox.showinfo("Genre Stories", stories)

        # Create a button for each genre file
        for filename in genre_files:
            genre_name = filename.replace('_stories.txt', '').capitalize()
            genre_button = tk.Button(existing_window, text=genre_name, command=lambda fn=filename: display_genre_stories(fn), bg='lightblue')
            genre_button.pack(pady=5)

        existing_window.mainloop()


    def choose_extras(self):
        extras_window = tk.Toplevel(self.root)
        extras_window.title("Choose Extras")
        extras_window.geometry("400x300")
        extras_window.configure(bg='lightblue')

        self.extras = None

        def set_extras():
            extras = simpledialog.askstring("Extras", "Enter any extra prompts:")
            if extras:
                self.extras = extras
                messagebox.showinfo("Extras Set", f"Extras: {self.extras}")
                extras_window.destroy()
                self.user_inputs['extras'] = self.extras
                self.check_submit_availability()

        set_button = tk.Button(extras_window, text="Set Extras", command=set_extras, bg='white')
        set_button.pack(pady=20)

        extras_window.mainloop()

    def show_my_stories(self):
        my_stories_window = tk.Toplevel(self.root)
        my_stories_window.title("My Stories")
        my_stories_window.geometry("400x400")
        my_stories_window.configure(bg='lightblue')

        # Define the user's story file path within the wordweaver folder
        user_folder_path = f"D:\\wordweaved\\{self.username}"
        story_file_path = os.path.join(user_folder_path, f"{self.username}_stories.txt")

        # Check if the story file exists
        if not os.path.exists(story_file_path):
            messagebox.showinfo("No Stories", "You have not generated any stories yet.")
            return

        # Load stories from the file, assuming each story is separated by "---\n"
        stories = []
        with open(story_file_path, 'r') as file:
            content = file.read()
            stories = content.split('---\n')

        def display_story(story):
            messagebox.showinfo("Story Content", story)

        for index, story in enumerate(stories):
            title = story.splitlines()[0] if story else f"Story {index + 1}"
            story_frame = tk.Frame(my_stories_window, bg='white')
            story_frame.pack(pady=5)
            story_label = tk.Label(story_frame, text=title, bg='white')
            story_label.pack(side=tk.LEFT)
            view_button = tk.Button(story_frame, text="View", command=lambda s=story: display_story(s), bg='lightblue')
            view_button.pack(side=tk.LEFT)

        my_stories_window.mainloop()


    def generate_story(self):
        # Ensure all fields are complete and initialized
        if not all(self.user_inputs.get(key) for key in ['genre', 'character', 'setting', 'length']):
            messagebox.showwarning("Incomplete Data", "Please complete all fields before submitting.")
            return

        story_content = ""  # Initialize story_content
        story_content += f"Genre: {', '.join(self.user_inputs['genre'])}\n"
        story_content += f"Setting: {self.user_inputs['setting']}\n"
        for char in self.user_inputs['character']:
            story_content += f"Character: {char['name']} - {char['personality']}\n"
        story_content += f"Length: {self.user_inputs['length']} words\n"
        if self.user_inputs.get('extras'):
            story_content += f"Extras: {self.user_inputs['extras']}\n"
        story_content += "\nOnce upon a time...\n"
        story_content += self.create_ai_generated_story(self.user_inputs)

        # Specify the main folder on the D: drive
        main_folder = r"D:\wordweaved"  # Set the folder to be on D:
        user_folder = os.path.join(main_folder, self.username)
        os.makedirs(user_folder, exist_ok=True)  # Create directory if it doesn't exist

        # Define story file path within user folder
        story_file_path = os.path.join(user_folder, f"{self.username}_stories.txt")

        # Append story content to the user's story file
        with open(story_file_path, "a") as story_file:
            story_file.write("\n" + "="*30 + "\n")  # Separator between stories
            story_file.write(story_content)

        # Insert story into the database
        self.cursor.execute('''INSERT INTO stories (title, author, genre, characters, setting, content)
            VALUES (%s, %s, %s, %s, %s, %s)''',
            ('Story Title', 'Author', ', '.join(self.user_inputs['genre']),
             str(self.user_inputs['character']), self.user_inputs['setting'], story_content))
        self.db.commit()

        messagebox.showinfo("Story Generated", "Your story has been generated and saved!")
        self.submit_button.config(state=tk.DISABLED)
        self.reset_inputs()


    def create_ai_generated_story(self, inputs):
        # Placeholder for actual AI story generation logic
        prompt = f"Genre: {', '.join(inputs['genre'])}\nSetting: {inputs['setting']}\n"
        for char in inputs['character']:
            prompt += f"Character: {char['name']} - {char['personality']}\n"
        prompt += f"Story: Once upon a time in {inputs['setting']}...\n"

        # Tokenize the prompt and generate the story
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        max_length = input_ids.shape[-1] + int(inputs['length'])  # Ensure length is integer

        outputs = self.model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2
        )

        # Decode the generated story
        generated_story = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_story

    def check_submit_availability(self):
        if all(self.user_inputs.values()):
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def reset_inputs(self):
        self.user_inputs = {
            'genre': None,
            'character': None,
            'setting': None,
            'length': None,
            'extras': None
        }

if __name__ == "__main__":
    root = tk.Tk()
    app = StoryWriterApp(root)
    root.mainloop()
