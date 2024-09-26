from flask import Flask, render_template, request, jsonify, redirect, url_for
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

@app.route("/", methods=["GET"])
def index():
    return render_template("BloodDonationCamp.html")

@app.route("/search", methods=["POST"])
def search():
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

if __name__ == "__main__":
    app.run(debug=True)
