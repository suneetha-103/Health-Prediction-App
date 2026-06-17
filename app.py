from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234", # Replace with your MySQL password
    database="health_db"
)

cursor = db.cursor()


# Simple AI Prediction Function
def predict_health(glucose, haemoglobin, cholesterol):
    if glucose > 140 or cholesterol > 240:
        return "High risk of diabetes or heart disease"
    elif haemoglobin < 12:
        return "Possible anemia"
    else:
        return "Healthy"


# Home Page
@app.route("/")
def index():
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    return render_template("index.html", patients=patients)


# Add Patient
@app.route("/add", methods=["POST"])
def add():
    full_name = request.form["full_name"]
    dob = request.form["dob"]
    email = request.form["email"]
    glucose = float(request.form["glucose"])
    haemoglobin = float(request.form["haemoglobin"])
    cholesterol = float(request.form["cholesterol"])

    remarks = predict_health(glucose, haemoglobin, cholesterol)

    sql = """
    INSERT INTO patients
    (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect("/")


# Delete Patient
@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))
    db.commit()
    return redirect("/")


# Edit Page
@app.route("/edit/<int:id>")
def edit(id):
    cursor.execute("SELECT * FROM patients WHERE id=%s", (id,))
    patient = cursor.fetchone()
    return render_template("edit.html", patient=patient)


# Update Patient
@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    full_name = request.form["full_name"]
    dob = request.form["dob"]
    email = request.form["email"]
    glucose = float(request.form["glucose"])
    haemoglobin = float(request.form["haemoglobin"])
    cholesterol = float(request.form["cholesterol"])

    remarks = predict_health(glucose, haemoglobin, cholesterol)

    sql = """
    UPDATE patients
    SET
    full_name=%s,
    dob=%s,
    email=%s,
    glucose=%s,
    haemoglobin=%s,
    cholesterol=%s,
    remarks=%s
    WHERE id=%s
    """

    values = (
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks,
        id
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)