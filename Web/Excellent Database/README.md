# Excellent Database

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/Web/Excellent%20Database/INSTALL.md)

### Description
I am in the process of making the next big social media platform but I have a history of implementing software insecurely. If you can get into the admin user, I will give you a flag. 

I'm testing out this new database architecture, and it's so beautiful I'll even let you look at the the code.

### Difficulty
2/10?

### Flag
`PCTF{Exc3l_is_th3_b3st_d4t4b4s3}`

### Hints
1. Excel formula injection

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This is a CSV injection attack, but specifically for Excel formulas.

Here is the important part of the code:
```python
<snip>

def add_user(username, password):
    DB = load_workbook(filename="db.xlsx")
    Users = DB["Users"]
    new_row = Users.max_row + 1
    Users[f"{USERNAMES}{new_row}"] = username
    Users[f"{PASSWORDS}{new_row}"] = password
    DB.save(filename="db.xlsx")

def read_db() -> pd.DataFrame:
    subprocess.Popen(["libreoffice", "--headless", "--convert-to", "csv", "db.xlsx"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).communicate()
    df = pd.read_csv("db.csv")
    return df


@app.route("/", methods=["POST", "GET"])
def base():
    if not session.get("username"):
        return redirect(url_for("login"))
    else:
        Users = read_db()
        username = session.get("username")
        password = Users.query(f"Username == '{username}'")["Password"].values[0]
        return render_template('index.html', name=username, password=password)


<snip>

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        Users = read_db()
        
        if username not in Users.Username.values:     
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('login'))
        elif password != Users.query(f"Username == '{username}'")["Password"].values[0]:
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('login'))

        session["username"] = request.form.get("username")
        return redirect("/")


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username = request.form.get("username")
        password = request.form.get("password")

        Users = read_db()
        if username in Users.Username.values:     
            flash('Username already exists')
            return redirect(url_for('signup'))
        else:
            add_user(username, password)
            session["username"] = username
            return redirect("/")
    else:
        return render_template('signup.html')


@app.route('/logout', methods=['GET'])
def logout():
    if request.method=='GET':
        username = session.get("username")
        session.pop('username', default=None)
        return redirect("/")


<snip>
```

We see that we are using a `.xlsx` (Excel) file as a database. We read from this database by converting it to a csv and loading it into a pandas DataFrame. I won't go into detail why, but that step is necessary for formulas in the Excel sheet to be evaluated instead of being sent back as a string (`=(7*7)` will become 49 and won't be returned as `"=(7*7)"`). 

Basically, if we put an Excel formula as our password, we should see the result after sign up.

When we sign up on the web app, we see our password is reflected back to us:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/excel_test.png" width=40%  height=40%></p>

Now let's put in an Excel formula, such as `=(7*7)`:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/excel_49.png" width=40%  height=40%></p>

Perfect. Now let's figure out what this Excel database looks like. Let's start with maybe what cells A1 and B1 hold (cause they're the first two cells on a sheet). Our password has to be `=CONCATENATE(A1, " ", B1)`:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/excel_table_headers.png" width=40%  height=40%></p>

Sweet, those look like table headers to me. You can use the same concatenate function to get all values of a certain row, but we can be almost positive the admin user's password will be the first in the table, thus it's location is at B2. Let's make our password `=B2`:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/excel_b2.png" width=40%  height=40%></p>

Now just log in as `admin:SuperStrongPassword` and go to the admin panel to see the flag:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/excel_admin.png" width=70%  height=70%></p>
