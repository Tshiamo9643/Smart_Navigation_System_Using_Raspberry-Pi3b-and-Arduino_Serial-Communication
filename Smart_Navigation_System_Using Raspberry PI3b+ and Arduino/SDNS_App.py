from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import sqlite3
import openpyxl
import os

app = Flask(__name__)
app.secret_key = '12345'  # Replace with your actual secret key

#1Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tshiamo846@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'xumtjycwhhigbott'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'tshiamo846@gmail.com'  # Replace with your email

mail = Mail(app)

def get_db_connection():
    conn = sqlite3.connect('project_data.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/')
def index():
    if 'user_type' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    try:
        latest_data = conn.execute('SELECT * FROM project_data ORDER BY timestamp DESC LIMIT 1').fetchone()
        if not latest_data:
            return "No data available."

        gps_data = []
        if latest_data['latitude'] and latest_data['longitude']:
            gps_data.append((latest_data['latitude'], latest_data['longitude'], latest_data['timestamp']))

        return render_template('Index.html', data=latest_data, gps_data=gps_data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Error fetching data."
    finally:
        conn.close()

@app.route('/all-data')
def all_data():
    if 'user_type' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project_data")
    all_data = cursor.fetchall()
    conn.close()
    return render_template('AllData.html', all_data=all_data)

@app.route('/send-email', methods=['POST'])
def send_email():
    if 'user_type' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project_data")
    data = cursor.fetchall()
    conn.close()

    # Create Excel file
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['ID', 'Timestamp', 'Distance 1', 'Distance 2', 'Distance 3', 'Latitude', 'Longitude', 'Date'])  # Add headers

    for row in data:
        ws.append(list(row))

    file_path = 'project_data.xlsx'
    wb.save(file_path)

    # Send email with the Excel file
    email = request.form['email']
    msg = Message('Project Data', recipients=[email])
    msg.body = 'Please find the attached project data in Excel format.'

    with app.open_resource(file_path) as fp:
        msg.attach(file_path, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', fp.read())

    try:
        mail.send(msg)
        flash('Email sent successfully!', 'success')
    except Exception as e:
        flash(f'Failed to send email: {e}', 'danger')

    os.remove(file_path)  # Clean up the file

    return redirect(url_for('all_data'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ? AND user_type = ?',
                            (username, password, user_type)).fetchone()
        conn.close()

        if user:
            session['user_type'] = user_type
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        if user_type not in ['admin', 'guardian']:
            flash('Invalid user type', 'danger')
            return redirect(url_for('register'))

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)',
                     (username, password, user_type))
        conn.commit()
        conn.close()

        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_type', None)
    return redirect(url_for('login'))

def create_users_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mail import Mail, Message
# import sqlite3
# import openpyxl
# import os
# 
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Replace with your actual secret key
# 
# # Email configuration
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'tshiamo846@gmail.com'  # Replace with your email
# app.config['MAIL_PASSWORD'] = 'xumtjycwhhigbott'   # Replace with your email password
# app.config['MAIL_DEFAULT_SENDER'] = 'tshiamo846@gmail.com'  # Replace with your email
# 
# mail = Mail(app)
# 
# def get_db_connection():
#     conn = sqlite3.connect('project_data.db')
#     conn.row_factory = sqlite3.Row  # This allows us to access columns by name
#     return conn
# 
# @app.route('/')
# def index():
#     conn = get_db_connection()
#     try:
#         latest_data = conn.execute('SELECT * FROM project_data ORDER BY timestamp DESC LIMIT 1').fetchone()
#         if not latest_data:
#             return "No data available."
# 
#         gps_data = []
#         if latest_data['latitude'] and latest_data['longitude']:
#             gps_data.append((latest_data['latitude'], latest_data['longitude'], latest_data['timestamp']))
# 
#         return render_template('Index.html', data=latest_data, gps_data=gps_data)
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return "Error fetching data."
#     finally:
#         conn.close()
# 
# @app.route('/all-data')
# def all_data():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM project_data")
#     all_data = cursor.fetchall()
#     conn.close()
#     return render_template('AllData.html', all_data=all_data)
# 
# @app.route('/send-email', methods=['POST'])
# def send_email():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM project_data")
#     data = cursor.fetchall()
#     conn.close()
# 
#     # Create Excel file
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.append(['ID', 'Timestamp', 'Distance 1', 'Distance 2', 'Distance 3', 'Latitude', 'Longitude', 'Date'])  # Add headers
# 
#     for row in data:
#         ws.append(list(row))
# 
#     file_path = 'project_data.xlsx'
#     wb.save(file_path)
# 
#     # Send email with the Excel file
#     email = request.form['email']
#     msg = Message('Project Data', recipients=[email])
#     msg.body = 'Please find the attached project data in Excel format.'
# 
#     with app.open_resource(file_path) as fp:
#         msg.attach(file_path, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', fp.read())
# 
#     try:
#         mail.send(msg)
#         flash('Email sent successfully!', 'success')
#     except Exception as e:
#         flash(f'Failed to send email: {e}', 'danger')
# 
#     os.remove(file_path)  # Clean up the file
# 
#     return redirect(url_for('all_data'))
# 
# if __name__ == '__main__':
#     app.run(debug=True)
# 

# from flask import Flask, render_template
# import sqlite3
# 
# app = Flask(__name__)
# 
# def get_db_connection():
#     conn = sqlite3.connect('project_data.db')
#     conn.row_factory = sqlite3.Row  # This allows us to access columns by name
#     return conn
# 
# @app.route('/')
# def index():
#     conn = get_db_connection()
#     try:
#         latest_data = conn.execute('SELECT * FROM project_data ORDER BY timestamp DESC LIMIT 1').fetchone()
#         if not latest_data:
#             return "No data available."
# 
#         gps_data = []
#         if latest_data['latitude'] and latest_data['longitude']:
#             gps_data.append((latest_data['latitude'], latest_data['longitude'], latest_data['timestamp']))
# 
#         return render_template('Index.html', data=latest_data, gps_data=gps_data)
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return "Error fetching data."
#     finally:
#         conn.close()
# 
# app.route('/all-data')
# def all_data():
#     conn = sqlite3.connect('project_data.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM project_data")
#     all_data = cursor.fetchall()
#     conn.close()
#     return render_template('AllData.html', all_data=all_data)
# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, render_template
# import sqlite3
# 
# app = Flask(__name__)
# 
# def get_db_connection():
#     conn = sqlite3.connect('project_data.db')
#     conn.row_factory = sqlite3.Row  # This allows us to access columns by name
#     return conn
# 
# @app.route('/')
# def index():
#     conn = get_db_connection()
#     try:
#         latest_data = conn.execute('SELECT * FROM project_data ORDER BY timestamp DESC LIMIT 1').fetchone()
#         if not latest_data:
#             return "No data available."
# 
#         gps_data = []
#         if latest_data['latitude'] and latest_data['longitude']:
#             gps_data.append((latest_data['latitude'], latest_data['longitude'], latest_data['timestamp']))
# 
#         return render_template('Index.html', data=latest_data, gps_data=gps_data)
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return "Error fetching data."
#     finally:
#         conn.close()
# 
# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template
# import sqlite3
# 
# app = Flask(__name__)
# 
# def get_db_connection():
#     conn = sqlite3.connect('project_data.db')
#     conn.row_factory = sqlite3.Row  # This allows us to access columns by name
#     return conn
# 
# @app.route('/')
# def index():
#     conn = get_db_connection()
#     try:
#         latest_data = conn.execute('SELECT * FROM project_data ORDER BY timestamp DESC LIMIT 1').fetchone()
#         if not latest_data:
#             return "No data available."
# 
#         gps_data = []
#         if latest_data['latitude'] and latest_data['longitude']:
#             gps_data.append((latest_data['latitude'], latest_data['longitude'], latest_data['timestamp']))
# 
#         return render_template('Index.html', data=latest_data, gps_data=gps_data)
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return "Error fetching data."
#     finally:
#         conn.close()
# 
# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template
# from sqliteDatabase import Database
# 
# app = Flask(__name__)
# 
# @app.route('/')
# def index():
#     db = Database('project_data.db')
#     latest_data = db.fetch_latest_data()
#     db.close()
# 
#     gps_data = []
#     if latest_data[5] and latest_data[6]:  # latitude and longitude
#         gps_data.append((latest_data[5], latest_data[6], latest_data[1]))  # latitude, longitude, timestamp
# 
#     return render_template('Index.html', data=latest_data, gps_data=gps_data)
# 
# if __name__ == '__main__':
#     app.run(debug=True)
