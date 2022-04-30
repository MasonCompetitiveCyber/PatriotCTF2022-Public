# ComicallyBadCrypto

For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/Crypto/ComicallyBadCrypto/INSTALL.md)

NOTE: Provide only `main.py` in the challenge

### Description
I don't know why this website needs an admin page. I guess I couldn't resist risking the unauthorized access of my super secret flag.

### Difficulty
Expert

### Flag
`PCTF{y0ur3_kind4_cr1ng3_f0r_s01ving_this_ng1}`

### Hints
1. Padding attack on CBC to leak secret
2. AES CBC is vulnerable to bit flipping attack

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This challenge requires a padding attack on AES in CBC mode to leak the secret cookie values and then use a bitflipping attack to give us admin. Here is the important part of the code:
```python
BS = AES.block_size
IV = get_random_bytes(BS)
KEY = get_random_bytes(BS)
BLUE = "#076185"
RAND = ''.join(random.choice(string.ascii_letters) for i in range(BS))

def make_cookie(color):
    cookie = f"color:{color}|{RAND}"
    cookie += confidential_settings
    return encrypt_cookie(cookie)

def encrypt_cookie(cookie: str) -> bytes:
    raw = pad(cookie.encode(), BS)
    cipher = AES.new(KEY, AES.MODE_CBC, IV).encrypt(raw)
    return b64encode(cipher)

def decrypt_cookie(cookie: bytes) -> bytes:
    cipher = b64decode(cookie)
    raw = AES.new(KEY, AES.MODE_CBC, IV).decrypt(cipher)
    return unpad(raw, BS)
    

@app.route("/", methods=["GET", "POST"])
def base():
    if request.method == "GET":
        if not request.cookies.get('session'):
            resp = make_response(render_template('index.html', color=BLUE))
            resp.set_cookie('session', make_cookie(BLUE))
            return resp
        else:
            cookie: bytes = decrypt_cookie(request.cookies.get('session'))
            color: string = cookie[6:13].decode()
            if admin(cookie) == True:
                return render_template('admin.html', color=color)
            else:
                return render_template('index.html', color=color)
    else:
        if request.form['color']:
            resp = make_response(redirect('/'))
            resp.set_cookie('session', make_cookie(request.form['color']))
            return resp
        else:
            return redirect("/")
```

Quick rundown of what's happening. If you GET the page without any cookie, one will be made for you that sets color to blue. If you have a cookie, it will decrypt it to set the background color to whatever your cookie's color setting is and will also check your cookie to see if you're admin or not.

The cookie is made by appending some "confidiential" cookie settings to the color setting and 16 bytes of a random string, like so: `color:#076185|RANDOMSTRINGABCD|somesecret:cookievalue`.

The vulnerability is that a secret is appended to input user controls, the color value. The first step is to leak this secret using a padding attack similar to that of the `Extremely Cool Book` challenge.

Let's start our script. First, just print a normal cookie after making a POST request setting the color:
```python
import requests
from base64 import b64decode

BS = 16 # block size
SERVER_ADDR = "http://127.0.0.1:5000"

def get_cookie(payload):
    data = {"color": payload}
    req = requests.post(SERVER_ADDR, data=data)
    cookiejar = req.history[0].cookies
    cookie = cookiejar.get_dict()['session']
    return cookie

print(get_cookie("#076185"))
```
`output: ErfklSJp/nB5k4hnr0HM1CFSGw7jxiU9N7T6RlVUsTDlFVKL00tmrtqEDP7n5y2I`

The base64 is 64 bytes which is 48 bytes decoded (base64 encodes 3 bytes into 4, so 64 * 3/4 = 48). 48 bytes means we have 3 blocks of 16 bytes (standard AES block size).

Let's visualize what this may look like:
```
color:#076185|--     "-" = random bytes                                       
--------------??     "?" = confidential secret (max 17 bytes, minimum 1 byte) 
???????????????X     "X" = paddng                                             
```
The color setting takes up 13 bytes, then a `|`, 16 bytes of random chars, and some amount of secret data. Since we are limited to 3 blocks, we know the secret must be of maximum size 48 - 13 - 1 - 16 - 1 = 17 (the last -1 is because the secret cannot fill the last block, as it would force a 4th block to be added of padding).  

Let's now determine the actual secret size. Let's add this to our script:
```python
def get_flag_len():
    payload = "A"
    min_BS = 3
    i = 1
    while True:
        length = len(b64decode(get_cookie(payload + "A"*i))) // BS
        if length > min_len:
            print(i+1)
            break
        i += 1
get_flag_len()
```
`output: 14`

So what does this mean? Let's visualize it again:
```
color:AAAAAAAAAA
AAAA|-----------   new block after 14 A's  
-----???????????   secret must be 11 bytes 
XXXXXXXXXXXXXXXX
```
A new block was added after we sent 14 A's as input. For this to happen, the last secret byte would have to have been the 16th byte of the 3rd block, forcing a 4th block of padding to be added. This means our secret must be 11 bytes.

Now, here's the idea to leak the secret. First let's call our overall unkown as `| + RAND + secret = 1 + 16 + 11 = 28 bytes`. 
```
|color:AAAAAAAAAA|  |color:AAAAAAAAAA|   first, send 41 A's to isolate first secret char 
|AAAAAAAAAAAAAAAA|  |AAAAAAAAAAAAAAAA|   then,  send 41 A's and a guess char (G)         
|AAAAAAAAAAAAAAA?|  |AAAAAAAAAAAAAAAG|   if block 3 of both ciphertexts match,             
|????????????????|  |????????????????|       our guess was correct                        
|???????????XXXXX|  |???????????XXXXX|
```

Repeat the step above after each guessed character, just remove one A and replace it with the succesfully guessed secret characters thus far. Let's finish the script, here's the full thing:
```python
import string
import requests
from base64 import b64decode

BS = 16 # block size
SERVER_ADDR = "http://127.0.0.1:5000"

def get_cookie(payload):
    data = {"color": payload}
    req = requests.post(SERVER_ADDR, data=data)
    cookiejar = req.history[0].cookies
    cookie = cookiejar.get_dict()['session']
    return cookie

# print(get_cookie("#076185"))

def get_flag_len():
    payload = "A"
    min_len = len(b64decode(get_cookie(payload))) // BS
    print("min block size", min_len)
    i = 1
    while True:
        length = len(b64decode(get_cookie(payload + "A"*i))) // BS
        if length > min_len:
            print(i+1)
            break
        i += 1
# get_flag_len()

guessed_secret = ""
secret_size = 28
init_push_size = 41

while len(guessed_secret) < secret_size:
    push = "A"*(init_push_size - len(guessed_secret))
    cookie = get_cookie(push)
    comp_block = cookie[BS*2:BS*3] # comparing the 3rd block

    for c in string.printable:
        payload = push + guessed_secret + c
        cookie = get_cookie(payload)
        if cookie[BS*2:BS*3] == comp_block:
            guessed_secret += c
            print(guessed_secret)
            break
```
Here's the output:
```console
$ python3 solve-cbc.py
|
|e
|ep
|epo
|epob
|epobu
|epobuF
|epobuFa
|epobuFaO
|epobuFaOn
|epobuFaOnI
|epobuFaOnIN
|epobuFaOnINQ
|epobuFaOnINQg
|epobuFaOnINQgt
|epobuFaOnINQgtq
|epobuFaOnINQgtqu
|epobuFaOnINQgtqu|
|epobuFaOnINQgtqu|i
|epobuFaOnINQgtqu|is
|epobuFaOnINQgtqu|is_
|epobuFaOnINQgtqu|is_a
|epobuFaOnINQgtqu|is_ad
|epobuFaOnINQgtqu|is_adm
|epobuFaOnINQgtqu|is_admi
|epobuFaOnINQgtqu|is_admin
|epobuFaOnINQgtqu|is_admin:
|epobuFaOnINQgtqu|is_admin:0
```

Yay! We got the confidential cookie setting that was appended to the color and RAND. Now, we just need that 0 to become a 1 to become admin. Luckliy for us, AES-CBC is vulnerable to bit flipping. 
<p align="center"><img src="https://resources.infosecinstitute.com/wp-content/uploads/082113_1459_CBCByteFlip3.jpg" width=70%  height=70%></p>

Basically, a change in byte N of one block will change byte N of the next block. Let's figure this out:
`t = p ⊕ d` where `t = target byte`, `p = previous block byte`, and `d = output of BlockCipherDecryption on the ciphertext byte corresponding to t`. Let's take a look at the equations below, where `p'` is a changed byte value for `p'` `value` is the byte value we want, and `t'` is the consequently changed byte value for `t`. 
```
If we set p' to the following, let's see what happens:
p' = t ⊕ value ⊕ p 

Start with base equation, then substitute and reduce:
t' = p'⊕ d
t' = t ⊕ value ⊕ p ⊕ d
t' = t ⊕ value ⊕ t
t' = value
```  
Would you look at that, if we set `p' = t ⊕ value ⊕ p` the resultant `t'` will be the value of the byte we want. In our case, we want to flip the `0` in `admin:0` to a `1`.

Let's work with the following cookie value:
```
color:#076185|ep
obuFaOnINQgtqu|i
s_admin:0XXXXXXX
```
`0` is the 9th byte of the 3rd block, so we must alter the 9th byte of the second block (byte 25, thus index 24).

Let's get the encrypted cookie value when sending just a post request for the color `#076185` (to make our above cookie value): `ErfklSJp/nB5k4hnr0HM1CFSGw7jxiU9N7T6RlVUsTDlFVKL00tmrtqEDP7n5y2I`

Now let's go through the steps to alter the cookie in such a way to flip the correct bit:
```python
>>> from base64 import b64decode, b64encode
>>> d = b64decode("ErfklSJp/nB5k4hnr0HM1CFSGw7jxiU9N7T6RlVUsTDlFVKL00tmrtqEDP7n5y2I")
# p' =  t ⊕ value ⊕ p      
>>> hex(0x00^0x01^d[24])
'0x36'
#   replace p with p' ↴
>>> new = d[:24] + b'\x36' + d[25:]
>>> b64encode(new).decode()
'ErfklSJp/nB5k4hnr0HM1CFSGw7jxiU9NrT6RlVUsTDlFVKL00tmrtqEDP7n5y2I'
```

Let's go to our browser, replace the cookie, and reload the page:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/solve-cbc.png" width=70%  height=70%></p>