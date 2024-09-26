from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Your database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "bloodbank",
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/display_requests')
def display_requests():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch data from the bloodrequests table
    cursor.execute("SELECT * FROM blood_requests")
    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    # Pass the fetched data to the reqdetails.html template
    return render_template('reqdetails.html', requests=requests)

if __name__ == '__main__':
    app.run(debug=True)
