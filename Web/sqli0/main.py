import sqlite3

from flask import Flask, render_template, request, session


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    db = sqlite3.connect("./sqli.db")
    cursor = db.cursor()
    if request.method == "GET":
        return render_template("index.html")
    else:
        print(request.form['username'])
        try:
            query = f"SELECT * FROM user WHERE username='{request.form['username']}' and password='{request.form['password']}'"
            rows = cursor.execute(query)
            if rows.fetchone():
                return render_template("dashborad.html", flag="PCTF{SQLI_iS_3@sy}")
            else:
                return render_template("login.html", error="Wrong username or password")
        except:
            return render_template('login.html')
if __name__ == '__main__':
    app.run(host="0.0.0.0")
