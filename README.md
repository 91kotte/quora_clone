# Quora-Like Django Q&A App

A simple web-based Q&A platform (like Quora), built using Django. Users can ask questions, post answers, view questions by others, and like answers.

---

## Features

- User registration 
- User login
- Post questions
- Search questions
- view questions posted by others 
- Able to answer questions posted by others
- able to Like/unlike answers posted by others
- User-friendly UI with Bootstrap
- Flash messages (alerts) support
- User to log out

---


## Setup Instructions ##
1. Clone the repo
git clone https://github.com/91kotte/quora_clone.git
cd quora_clone

2. Create a virtual environment and activate it
python -m venv env
source env/bin/activate  # For Linux/macOS
env\Scripts\activate     # For Windows

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py migrate
python manage.py makemigrations

5. Run the development server
python manage.py runserver


