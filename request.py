from flask import Flask, render_template, request, redirect, url_for
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

# Route to handle form submission
@app.route('/submit_blood_request', methods=['POST'])
def submit_blood_request():
    if request.method == 'POST':
        # Get form data
        blood_group = request.form['BloodGroup']
        quantity = request.form['quantity']
        blood_component = request.form['bloodComponent']
        hospital_name = request.form['hospitalName']
        date = request.form['Date']
        phone_number = request.form['PhoneNumber']
        requested_by = request.form['RequestedBy']
        comments = request.form['comments']
        conn = get_db_connection()
        cursor = conn.cursor()
        # Prepare SQL statement
        sql = "INSERT INTO blood_requests (BloodGroup, Quantity, BloodComponent, HospitalName, Date, PhoneNumber, RequestedBy, AdditionalComments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (blood_group, quantity, blood_component, hospital_name, date, phone_number, requested_by, comments)
        try:
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()

            # Redirect back to the blood request form after submission
            return redirect(url_for('blood_request_form'))

        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")
            conn.rollback()

            # Close cursor and connection
            cursor.close()
            conn.close()

            # Redirect to an error page or handle the error as needed

# Route for rendering the blood request form

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/bloodrequestform')
def blood_request_form():
    return render_template('bloodrequestform.html')

@app.route('/emergency-requests')
def emergency_requests():
    # You can add any additional logic or data retrieval needed for this page
    return render_template('emgreq.html')

if __name__ == '__main__':
    app.run(debug=True)  # Change the port number as needed

