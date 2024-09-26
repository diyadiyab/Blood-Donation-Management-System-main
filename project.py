from flask import Flask, render_template, request, jsonify, session, redirect, url_for

import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
# Donor registration
def process_data(name, age, blood_group, mobile_number, weight, state, district, last_donation_date, medicines):
    return (name, age, blood_group, mobile_number, weight, state, district, last_donation_date, medicines)

# Validation functions...

@app.route("/donorreg", methods=["GET", "POST"])
def register_donor():
    error_message = None
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        try:
            name = request.form["name"]
            age = request.form["age"]
            blood_group = request.form["blood_group"]
            mobile_number = request.form["mobile_number"]
            weight = request.form["weight"]
            state = request.form["state"]
            district = request.form["district"]
            last_donation_date = request.form["last_donation_date"]
            medicines = request.form["medicines"]

            # Validation checks...

            data = process_data(name, age, blood_group, mobile_number, weight, state, district, last_donation_date, medicines)
            sql = "INSERT INTO donors (name, age, blood_group, mobile_number, weight, state, district, last_donation_date, medicines) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            cursor.execute(sql, data)
            conn.commit()

            print("Data inserted successfully!")

            cursor.close()
            conn.close()

            return redirect(url_for('thank_you'))
        except mysql.connector.Error as err:
            conn.rollback()
            error_message = f"Error: {err.msg}"
            print(f"Error inserting data: {err}")
            return render_template("Registrationform.html", error_message=error_message)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return render_template("Registrationform.html", error_message="An unexpected error occurred.")
        finally:
            cursor.close()
            conn.close()

    return render_template("Registrationform.html")
@app.route("/thank-you")
def thank_you():
    return render_template("thank.html", success_message="Thank you for registering!")
@app.route('/donorreg')
def blood_registration_form():
    return render_template('Registrationform.html')

#Blood request
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
        sql = "INSERT INTO bloodrequests (BloodGroup, Quantity, BloodComponent, HospitalName, DateRequested, PhoneNumber, RequestedBy, AdditionalComments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (blood_group, quantity, blood_component, hospital_name, date, phone_number, requested_by, comments)
    
        try:
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()

            # Redirect back to the blood request form after submission
            return redirect(url_for('request_success'))

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

@app.route('/requestsuccess')
def request_success():
    return render_template('requestsuccess.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

#bloodavailability


@app.route("/availability", methods=["GET"])
def index():
    return render_template("bloodavailability.html")

@app.route("/search", methods=["POST"])
def search():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        state = request.json.get("state")
        district = request.json.get("district")
        blood_group = request.json.get("bloodGroup")
        blood_component = request.json.get("bloodComponent")

        query = "SELECT * FROM BloodAvailabilityTable WHERE state = %s AND district = %s AND blood_group = %s AND blood_component = %s"
        cursor.execute(query, (state, district, blood_group, blood_component))
        results = cursor.fetchall()
        print(f"Fetched results: {results}")
        cursor.close()
        conn.close()

        if results:
            print(f"Results found: {results}")
            session['search_results'] = results
            return jsonify(results=results)
        else:
            print("No results found in the database.")
            return jsonify(results=[], message="No results found.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify(error=str(e))

@app.route("/availabilityresult", methods=["GET"])
@app.route("/availabilityresult", methods=["GET"])
def availability_result():
    search_results = session.get('search_results')
    if search_results:
        # Ensure the data structure is in a list of dictionaries, similar to your mock data in JavaScript
        formatted_results = [
            {
                'ID_NO': row[0],  # Replace with respective column indexes from your database query result
                'Hospital_name': row[1],
                'Donor_name': row[2],
                'Contact_no': row[3],
                'state': row[4],
                'district': row[5],
                'blood_group': row[6],
                'blood_component': row[7]
            }
            for row in search_results
        ]
        return render_template("availabilityresult.html", results=formatted_results)
    else:
        return render_template("availabilityresult.html", results=[])

#blooddonationcamp

@app.route("/donationcamp", methods=["GET"])
def campdetails():
    return render_template("BloodDonationCamp.html")

@app.route("/searchh", methods=["POST"])
def searchh():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        district = request.form.get("district")

        query = "SELECT * FROM camp WHERE district = %s"
        cursor.execute(query, (district,))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        if results:
            return render_template("campresult.html", results=results)
        else:
            return jsonify(results=[], message="No results found for the selected district.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify(error="An unexpected error occurred.")

@app.route('/blood_donation_camp', methods=['GET', 'POST'])
def blood_donation_camp():
    if request.method == 'POST':
        state = request.form['state']
        district = request.form['district']
        return redirect(url_for('show_camp_result', state=state, district=district))
    return render_template('BloodDonationCamp.html')

@app.route('/campresult')
def show_camp_result():
    state = request.args.get('state')
    district = request.args.get('district')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM camp WHERE district = %s"
        cursor.execute(query, (district,))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('campresult.html', state=state, district=district, results=results)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify(error="An unexpected error occurred.")
    
@app.route('/display_requests')
def display_requests():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch data from the bloodrequests table
    cursor.execute("SELECT * FROM bloodrequests")
    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    # Pass the fetched data to the reqdetails.html template
    return render_template('reqdetails.html', requests=requests)

if __name__ == "__main__":
    app.run(debug=True)

