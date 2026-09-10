# WordWeaver 📖

**WordWeaver** is a desktop AI story-generation application built with Python. It allows users to create short stories by selecting a genre, defining characters, choosing a setting, specifying a target word count, and optionally adding extra prompts.

The application combines a **Tkinter GUI**, **GPT-2 text generation**, and **MySQL** for user accounts and story records.

## ✨ Features

- User registration and login
- SHA-256 password hashing for stored passwords
- AI-powered story generation using GPT-2
- Genre selection
- Custom character names, personalities, and optional roles
- Custom story setting
- Target story length with safe limits
- Optional extra prompts
- Save generated stories to MySQL
- Save stories to local text files
- View personal story history
- Browse generated stories by genre
- Input validation and user-friendly error messages

## 🛠️ Tech Stack

- **Python 3.11**
- **Tkinter** — desktop GUI
- **MySQL** — database
- **mysql-connector-python** — MySQL connection
- **PyTorch** — model inference
- **Hugging Face Transformers** — GPT-2 model and tokenizer

## 📁 Project Structure

```text
wordweaver/
├── main.py
├── requirements.txt
├── schema.sql
├── README.md
├── .gitignore
├── screenshots/
└── stories/              # Created automatically for generated stories
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/runey-jesly/WordWeaver.git
cd WordwWeaver
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up MySQL

Make sure MySQL Server is installed and running.

Run:

```bash
mysql -u root -p < schema.sql
```

The schema creates the `wordweaver` database and the required `users` and `stories` tables.

### 4. Configure database credentials

The application uses these environment variables:

```text
WORDWEAVER_DB_HOST
WORDWEAVER_DB_USER
WORDWEAVER_DB_PASSWORD
WORDWEAVER_DB_NAME
```
If they are not set, the defaults are:
Host: localhost
User: root
Database: wordweaver

**For GitHub, do not commit real database passwords.** Set your own environment variables if your local MySQL password is different.

### 5. Run the application

```bash
python main.py
```

On the first run, Hugging Face downloads the GPT-2 model. Internet access is required for the initial download.

## 🧠 How WordWeaver Works

```text
User
  ↓
Login / Registration
  ↓
Select Story Details
  ├── Genre
  ├── Characters
  ├── Setting
  ├── Word Length
  └── Optional Extras
  ↓
GPT-2 Story Generation
  ↓
Save Story
  ├── MySQL Database
  └── Local Story Files
  ↓
View My Stories / Existing Stories
```

## 🤖 AI Story Generation

WordWeaver uses the **GPT-2** language model through Hugging Face Transformers.

The selected genre, setting, characters, and optional extra prompt are combined into a text prompt. GPT-2 generates the continuation, which is then trimmed to the requested target word count.

The application limits the requested story length to help stay within GPT-2's context window.

> **Note:** GPT-2 generates text in tokens rather than exact words, so the requested word count is treated as a target rather than a mathematical guarantee.

## 🗄️ Data Storage

WordWeaver uses MySQL to store:

- User accounts
- Story title
- Author
- Genre
- Characters
- Setting
- Generated story content

Generated text files are stored inside the project's `stories/` directory, so the application does not depend on a specific drive such as `D:\`.

## 🔐 Security Note

Passwords are hashed with SHA-256 before being stored in the database.

For a production application, a password-specific salted hashing algorithm such as **bcrypt** or **Argon2** would be preferable.

Database credentials should also be provided through environment variables rather than committed to source code.

## 📸 Screenshots

The `screenshots/` folder contains example screenshots of the application workflow.

## 🚀 Future Enhancements

- Password reset and account management
- Stronger password hashing with bcrypt or Argon2
- Better story-reading interface with scrolling
- Export stories as PDF or text
- Text-to-speech
- Multi-language story generation
- Cloud storage
- Collaborative story writing
- More advanced and modern GUI design

## 📄 License

This project is intended primarily as an educational/college project.
