import sqlite3
from flask import Flask, render_template, request

global_iid = None
global_name = None
global_email = None
global_password = None
global_phone = None
global_bth = None

conn = sqlite3.connect('membership.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS members (
iid INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
email TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
phone TEXT,
birthdate TEXT);''')
conn.commit()
cursor.close()
conn.close()

conn = sqlite3.connect('membership.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM members")
exsit = cursor.fetchone()[0]
if exsit:
    cursor.execute('DELETE FROM members')

cursor.execute('''INSERT OR IGNORE INTO members (username, email, password,
               phone, birthdate) VALUES (?, ?, ?, ?, ?)''', ('admin',
               'admin@example.com', 'admin123', '0912345678', '1990-01-01'))
conn.commit()
cursor.close()
conn.close()

app = Flask(__name__)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    '''edit_profile'''
    if request.method == 'POST':
        global global_email
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        birthdate = request.form['bth']

        conn = sqlite3.connect('membership.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE email = ?", (email,))
        exist = cursor.fetchone()
        if exist and global_email != email:  # account used?
            conn.close()
            return render_template('error.html', message='電子郵件已被使用')
        else:
            global global_name, global_password, global_phone, global_bth
            global_name = username
            global_email = email
            global_password = password
            global_phone = phone
            global_bth = birthdate
            cursor.execute('''UPDATE members SET username = ?, email = ?,
                           password = ?, phone = ?, birthdate = ?
                           WHERE iid = ?''', (username, email, password,
                           phone, birthdate, global_iid))
            conn.commit()
            cursor.close()
            conn.close()
            return render_template('welcome.html', message=global_name)

    return render_template('edit_profile.html')


@app.route('/', endpoint='index')
def index():
    '''home page'''
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''login'''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email)
        print(password)
        conn = sqlite3.connect('membership.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE email = ?", (email,))
        exist = cursor.fetchone()

        if exist:  # is member?
            global global_iid, global_name, global_email, global_password
            global global_phone, global_bth
            global_iid = exist[0]
            global_name = exist[1]
            global_email = exist[2]
            global_password = exist[3]
            global_phone = exist[4]
            global_bth = exist[5]
            conn.close()
            return render_template('welcome.html', message=global_name)
        else:
            print("not exist")
            conn.close()
            return render_template('error.html', message='電子郵件或密碼錯誤')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''register'''
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        birthdate = request.form['bth']
        print(username)
        print(email)
        print(password)
        print(phone)
        print(birthdate)
        conn = sqlite3.connect('membership.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE email = ?", (email,))
        exist = cursor.fetchone()

        if exist:  # account exist?
            conn.close()
            return render_template('error.html', message='用戶名已存在')
        else:
            cursor.execute('''INSERT INTO members (username, email, password,
                           phone, birthdate) VALUES (?, ?, ?, ?, ?)''',
                           (username, email, password, phone, birthdate))
            conn.commit()
            cursor.close()
            conn.close()
            return render_template('login.html')

    return render_template('register.html')


@app.route('/welcome')
def welcome():
    '''welcome'''
    return render_template('welcome.html', message=global_name)


@app.route('/delete', methods=['POST'])
def delete():
    '''delete warrning'''
    global global_iid
    conn = sqlite3.connect('membership.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM members WHERE iid = ?', (global_iid,))
    conn.commit()
    cursor.close()
    conn.close()

    global global_name, global_email, global_password, global_phone, global_bth
    global_iid = None
    global_name = None
    global_email = None
    global_password = None
    global_phone = None
    global_bth = None
    return render_template('index.html')
