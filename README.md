# Lifestyle Survey App 🍕📊

A simple Flask application for collecting and analyzing lifestyle preferences.

## Features ✨
- 📝 Survey form with personal details and preferences
- ✅ Client-side and server-side validation
- 💾 SQLite database storage
- 📊 Automated statistics calculation
- 🎨 Clean responsive interface

## Installation 🛠️
1. Clone the repository:
   ```
   git clone https://github.com/ThomasKarabo/survey-app.git
   cd survey-app```

2. Install requirements
    ```
    pip install -r requirements.txt```

## Usage
1. Initialize the database:
``` python app.py```
(This will create survey.db automatically)

2. Access the app in your browser:
http://localhost:5000

## File Structure 📂
survey_app/

├── app.py             # Main application logic

├── survey.db          # Database (auto-created)

├── static/

│   └── style.css      # Stylesheet

├── templates/

│   ├── home.html      # Survey form

│   └── results.html   # Statistics view

└── README.md          # This file

## Calculations Performed 🧮
- Total survey count

- Average participant age

- Oldest/youngest participants

- Food preference percentages (Pizza, Pasta, Pap and Wors)

- Average ratings for activities (1-5 scale)
