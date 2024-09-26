from flask import Flask, render_template, request, jsonify, session
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

@app.route("/", methods=["GET"])
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
            return jsonify(results=[], message="No results found.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify(error="An unexpected error occurred.")

@app.route("/availabilityresult", methods=["GET"])
def availability_result():
    search_results = session.get('search_results')
    return render_template("availabilityresult.html", results=search_results)

if __name__ == "__main__":
    app.run(debug=True)