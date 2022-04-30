
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
    return render_template("dashboard.html")

def detect_sqli(username, password):
    filters = ['or', 'and', 'admin']

    for filte in filters:
        if filte in password or filte in username:
            return (True, filte)
    else:
        return (False, )


@app.route('/login', methods=["GET", "POST"])
def login():
    db = sqlite3.connect("./sqli.db")
    cursor = db.cursor()
    if request.method == "GET":
        return render_template("login.html")
    else:
        filte = detect_sqli(request.form['password'] , request.form['username'])
        if filte[0]:
            print("SQL injection detected")
            return render_template("login.html", error="SQL injection Deteced: "+filte[1])
        query = f"SELECT * FROM user WHERE username='{request.form['username']}' and password='{request.form['password']}'"
        print(query)
        rows = cursor.execute(query)
        user = rows.fetchone()
        if user:
            print(user)
            if user[0] == 'admin':
                return render_template("dashborad.html", flag="PCTF{w0rld_0f_sQl_8kdw7}")
            else:
                return render_template("dashborad.html", flag="PCTF{f1l7ers_n0t_s3cur3}")
        else:
            return render_template("login.html", error="Wrong username or password")

if __name__ == '__main__':
    app.run(host="0.0.0.0")

