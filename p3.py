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

def process_data(name, age, blood_group, mobile_number, weight, state, district, last_donation_date, medicines):
    return (name, age, blood_group, mobile_number, weight, state, district, last_donation_date, medicines)

# Validation functions...

@app.route("/", methods=["GET", "POST"])
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

if __name__ == "__main__":
    app.run(debug=True)

