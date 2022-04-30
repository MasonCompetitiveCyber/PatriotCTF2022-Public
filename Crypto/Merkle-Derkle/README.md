# Merkle-Derkle

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/Crypto/Merkle-Derkle/INSTALL.md)

NOTE: Provide only `main.py` in the challenge

### Description
I'm new to web development, so I'm still trying to figure out how to properly secure and authenticate user sessions. If you find a way to become admin, I will give you the flag in the `admin.html` page

### Difficulty
5/10?

### Flag
`PCTF{c4p4c10us_3xtr3m1s}`

### Hints
1. Attack based on prepended secret in a hash
2. Hash legnth extension

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This challenge is vulnerable to a hash length extension attack. Here is the relevant section of the server code:
```python
letters = string.ascii_letters
secret = ''.join(random.choice(letters) for i in range(random.randint(15,35)))

def new_user():
    user = "admin=False"
    data = secret + user
    mac = sha1(data.encode()).hexdigest()
    cookie_val = user.encode().hex() + "." + mac
    return cookie_val

def validate(cookie):
    user_hex = cookie.split(".")[0]
    user = bytes.fromhex(user_hex)
    data = secret.encode() + user
    
    cookie_mac = cookie.split(".")[1]
    if cookie_mac != sha1(data).hexdigest():
        raise Exception("MAC does not match!")
    
    return ast.literal_eval(user.split(b"=")[-1].decode()) 

@app.route("/", methods=["GET"])
def base():
    if not request.cookies.get('auth'):
        resp = make_response(render_template('index.html'))
        resp.set_cookie('auth', new_user())
        return resp
    else:
        try:
            admin = validate(request.cookies.get('auth'))
        except Exception as e:
            flash(str(e), 'danger')
            return render_template('index.html')

        if admin:
            return render_template('admin.html')
        else:
            return render_template('index.html')
```

We see that an `auth` cookie is set to the hex of `admin=False` separated by a period from the SHA1 hash of a secret between 15-35 chars prepended to `admin=False`. This is an insecure way to implement a MAC because the secret is prepended to user-controlled input (the user can send anything before the `.` and it will be decoded from hex and taken as the user identification string). This means we have a hash length extension vulnerability. 

I can't do a better job of explaining the attack than the following three blogs, so just read those if you want to understand what's happening:
- https://blog.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks
- https://journal.batard.info/post/2011/03/04/exploiting-sha-1-signed-messages
- https://blog.skullsecurity.org/2014/plaidctf-web-150-mtpox-hash-extension-attack

The tool [`hash_extender`](https://github.com/iagox86/hash_extender) will do all the work for us. We just need to tell it the initial data, initial hash of that data, the length of the secret prepended to the data, the type of hash, and what we want to append. 

We want to append `=True` because of this section in the code splitting the user string: `return ast.literal_eval(user.split(b"=")[-1].decode())`. Here is an example of the output from the tool:
```console
$hash_extender -d="admin=False" -s="b73beb3af33ddffa4572253f464b9e44acfa4424" -f=sha1 -a "=True" -l 33
Type: sha1
Secret length: 33
New signature: e94525e0d87e439340ee9cb5ebc39e894af5cf60
New string: 61646d696e3d46616c736580000000000000000000000000000000000001603d54727565
```
The only thing we do not know is the length, as it is a number between 15-35. We just have to brute force it then.

Here is my solution bash script:
```bash
#!/bin/bash

# get initial cookie
init_cookie=$(curl -s -D - -o /dev/null http://localhost:5000 | sed -nr 's/.*auth=(.*);.*/\1/p')
init_hash=$(echo $init_cookie | cut -d "." -f 2)

# brute force lengths from 15-35
for i in $(seq 15 35)
do
    echo $i
    # use hash_extender for new string and signature
    out=$(/opt/tools/hash_extender/hash_extender -d="admin=False" -s=$init_hash -f=sha1 -a "=True" -l $i)
    sig=$(echo $out | cut -d " " -f 8) # cut out signature from output
    string=$(echo $out | cut -d " " -f 11) # cut out new string from output
    cookie=$(echo "$string.$sig") # set cookie to string.signature
    # make request and see if PCTF is in output
    if curl -s 'http://localhost:5000' -H "Cookie: auth=$cookie" | grep "PCTF"; then
        break
    fi
done
```

Run it:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/merkle-solve.png" width=40%  height=40%></p>