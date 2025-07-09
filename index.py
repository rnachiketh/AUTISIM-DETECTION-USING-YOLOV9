from flask import Flask, render_template, request, session
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from ultralytics import YOLO
import joblib

app = Flask(__name__)
app.secret_key = "abc"

# Load models
autism_model = joblib.load("models/autism_model.pkl")
yolo_model = YOLO("models/best.pt")

def init_db():
    with sqlite3.connect("autism_detection.db") as con:
        con.execute("""CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            username TEXT PRIMARY KEY,
            passwd TEXT,
            email TEXT,
            mobile TEXT
        )""")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        name = request.form["name"]
        uid = request.form["uid"]
        pwd = request.form["pwd"]
        email = request.form["email"]
        mno = request.form["mno"]

        with sqlite3.connect("autism_detection.db") as con:
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (uid,))
            count = cursor.fetchone()[0]
            if count == 1:
                return render_template("user_register.html", msg="Username Already Exists")
            else:
                hashed_pwd = generate_password_hash(pwd)
                cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (name, uid, hashed_pwd, email, mno))
                con.commit()
                return render_template("user_login.html", msg1="Registered Successfully")
    return render_template("user_register.html")

@app.route("/userlogin_check", methods=["POST"])
def userlogin_check():
    uid = request.form["uid"]
    pwd = request.form["pwd"]

    with sqlite3.connect("autism_detection.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT passwd FROM users WHERE username=?", (uid,))
        res = cursor.fetchone()
        if res and check_password_hash(res[0], pwd):
            session["uid"] = uid
            return render_template("user_home.html")
        else:
            return render_template("user_login.html", msg2="Invalid Credentials")

@app.route("/user_home")
def user_home():
    if "uid" in session:
        return render_template("user_home.html")
    return render_template("user_login.html", msg2="Please login first")

@app.route("/user_predict", methods=["GET", "POST"])
def user_predict():
    if "uid" not in session:
        return render_template("user_login.html", msg2="Please login first")

    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return render_template("user_predict.html", msg="No file selected")

        filename = secure_filename(file.filename)
        filepath = os.path.join("static", filename)
        file.save(filepath)

        result = autism_model.predict([filepath])
        msg = "Autistic" if result[0] == 1 else "Non-Autistic"
        return render_template("user_predict.html", msg=msg, img=filename)

    return render_template("user_predict.html")

@app.route("/yolo_detect", methods=["POST"])
def yolo_detect():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join("static", filename)
    file.save(filepath)

    results = yolo_model(filepath)
    boxes = results[0].boxes
    msg = f"YOLOv9 detected {len(boxes)} object(s)." if boxes else "No detections"
    return render_template("user_predict.html", msg=msg, img=filename)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
