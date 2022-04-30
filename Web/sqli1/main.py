
import sqlite3
import os
from flask import Flask, render_template, request, session


app = Flask(__name__)
app.SECRET_KEY = os.urandom(16)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashborad.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    db = sqlite3.connect("./sqli.db")
    cursor = db.cursor()
    if request.method == "GET":
        return render_template("login.html")
    else:
        try:
            query = f"SELECT * FROM user WHERE username='{request.form['username']}' and password='{request.form['password']}'"
            rows = cursor.execute(query)
            user = rows.fetchone()
            if user:
                if user[0] == 'admin':
                    return render_template("dashborad.html", flag="PCTF{K33p_G0ing_U_G07_7h1s}")
                else:
                    return render_template("dashborad.html", flag="flag{NOT_gonna_be_that_easy_this_time}")
            else:
                return render_template("login.html", error="Wrong username or password")
        except:
            return render_template('login.html')
if __name__ == '__main__':
    app.run(host="0.0.0.0")

