from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

my_db = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= 'thaalibiya',
    database= 'testdb'
)

def get_db_connection():
    return my_db

@app.route('/')
def index():
    if 'nom' in session :
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('INSERT INTO user VALUES (%s, %s, %s)', (email, password, username))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index'))

    except Exception as e:
        print(f"Error: {str(e)}")
        return "An error occurred while processing your request."

    
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the username already exists
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already exists. Choose another username."
        else:
            # Insert the new user into the database
            cursor.execute('INSERT INTO user (email, password, username) VALUES (%s, %s, %s)', (email, password, username))
            conn.commit()

            return "User registered successfully."

    except Exception as e:
        print(f"Error: {str(e)}")
        return "An error occurred while processing your request."
    
    finally :
        cursor.close()
        conn.close()


@app.route('/update_password', methods=['POST'])
def update_password():
    print("Session:", session)
    
    if 'username' in session:
        new_password = request.form['new_password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Update the user's password
            cursor.execute('UPDATE user SET password = %s WHERE username = %s', (new_password, session['username']))
            conn.commit()

            return "Password updated successfully."

        except Exception as e:
            print(f"Error: {str(e)}")
            return "An error occurred while processing your request."

        finally:
            cursor.close()
            conn.close()
    else:
        return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'username' in session :
        return render_template('dashboard.html', username = session['username'])
    else :
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    print("Logging out...")
    session.pop('username', None)
    print("Logged out.")
    return redirect(url_for('index'))

if __name__ == '__main__' :
    app.run(debug= True)
