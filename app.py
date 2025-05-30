from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def get_db():
    conn = sqlite3.connect('survey.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS surveys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            pizza INTEGER DEFAULT 0,
            pasta INTEGER DEFAULT 0,
            pap_wors INTEGER DEFAULT 0,
            other_food TEXT,
            movies_rating INTEGER NOT NULL,
            radio_rating INTEGER NOT NULL,
            eat_out_rating INTEGER NOT NULL,
            tv_rating INTEGER NOT NULL
        )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    
    # Calculate age for validation
    birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d')
    age = (datetime.now() - birth_date).days // 365
    
    if age < 5 or age > 120:
        return "Age must be between 5 and 120", 400
    
    # Save to database
    conn = get_db()
    conn.execute('''
    INSERT INTO surveys (
        full_name, email, birth_date, contact_number,
        pizza, pasta, pap_wors, other_food,
        movies_rating, radio_rating, eat_out_rating, tv_rating
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['full_name'], data['email'], data['birth_date'], data['contact_number'],
        1 if 'pizza' in data else 0,
        1 if 'pasta' in data else 0,
        1 if 'pap_wors' in data else 0,
        data.get('other_food', ''),
        data['movies_rating'], data['radio_rating'], 
        data['eat_out_rating'], data['tv_rating']
    ))
    conn.commit()
    return redirect(url_for('results'))

@app.route('/results')
def results():
    conn = get_db()
    surveys = conn.execute('SELECT * FROM surveys').fetchall()
    
    if not surveys:
        return render_template('results.html', no_data=True)
    
    # Calculate stats
    total = len(surveys)
    ages = [calculate_age(datetime.strptime(s['birth_date'], '%Y-%m-%d')) for s in surveys]
    pizza_count = sum(1 for s in surveys if s['pizza'])
    pasta_count = sum(1 for s in surveys if s['pasta'])
    pap_wors_count = sum(1 for s in surveys if s['pap_wors'])
    
    # Rating averages (1-5 scale)
    movies_avg = round(sum(s['movies_rating'] for s in surveys) / total, 1)
    radio_avg = round(sum(s['radio_rating'] for s in surveys) / total, 1)
    eat_out_avg = round(sum(s['eat_out_rating'] for s in surveys) / total, 1)
    tv_avg = round(sum(s['tv_rating'] for s in surveys) / total, 1)
    
    stats = {
        'total': total,
        'avg_age': round(sum(ages) / total, 1),
        'max_age': max(ages),
        'min_age': min(ages),
        # Food percentages (rounded to 1 decimal)
        'pizza_percent': round((pizza_count / total) * 100, 1),
        'pasta_percent': round((pasta_count / total) * 100, 1),
        'pap_wors_percent': round((pap_wors_count / total) * 100, 1),
        # Rating averages
        'movies_avg': movies_avg,
        'radio_avg': radio_avg,
        'eat_out_avg': eat_out_avg,
        'tv_avg': tv_avg
    }
    return render_template('results.html', stats=stats)

def calculate_age(birth_date):
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)