# Extremely Cool Book

NOTE: `server.py` is what is shared with players (fake flag), `ECB.py` is the real server w/ the flag

### Description
Can you authenticate yourself to this service and steal the secret access code?

Connect with `nc <IP> 8000`

### Difficulty
Expert

### Flag
`PCTF{p4ti3nc3_my_p4d4w4n}`

### Hints
Research attacking AES in ECB mode

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This challenge deals with abusing AES padding in ECB mode. Here is the relevant section of the server code:
```python
KEY = get_random_bytes(16)
FLAG = "real_flag_is_defined_here"

def encrypt(username,req):
    cipher = AES.new(KEY, AES.MODE_ECB)
    message = f"{username}, here is your top secret access code for today: {FLAG}"
    pad = 16 - (len(message) % 16)
    plaintext = message + (chr(pad)*pad)
    return cipher.encrypt(plaintext.encode()).hex().encode()

def validate(req):
    req.sendall(b'Please input your username to verify your identity. \n~> ')
    username = req.recv(256).decode('ascii')
    if username.split("\n")[0] == "admin":
        enc_message = encrypt(username,req)
        req.sendall(b'\n' + b'-' * 64 + b'\n')
        req.sendall(b"Here is you encrypted message:\n\n")
        req.sendall(enc_message + b'\n')
        return True
    return False

class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        result = validate(self.request)
        if result is False:
            self.request.sendall(b'Invalid username.\n')
```

First off, we need to pass the username check to get the encrypted message back. All we need to do is send `admin\n` and it will pass. It will also pass with `admin\nOTHERDATA`, which is important later.

The `encrypt()` function is using AES in ECB mode to encrypt a message containing the username we provide and the flag. This means we have control over the message to be encrypted, affecting the placement of the rest of the message within blocks and padding, including the flag.

Let's just connect to it normally and see what we get:
```console
$ nc localhost 8000                                                                               1 ⨯
Please input your username to verify your identity. 
~> admin

----------------------------------------------------------------
Here is you encrypted message:

2018d27fc834c55da56a78be1f6011482e09ce6f4e9eba78b343b21471864e85df606b6aa8bdc2725c2d446f96e2c24d7004bfb1c9a41240e40a84ec580c6ce9b16b3556e88af4f27028a30dddf1c66a93ad8398e8027c8d872ffb3f023a4d95
```

This encrypted message has a lenght of 192 hex characters, so 96 bytes (2 hex = 1 byte). The blocks in AES ECB are 16 bytes, so this means we have 96/16 = 6 blocks. Let's try to visualize this:

```
|admin%, here is |  % = \n
|your top secret |
|access code for |  
|today: FLAGFLAGF|    
|LAGFLAGFLAGFLAGF|  
|XXXXXXXXXXXXXXXX|  X = padding (\xf in this case)
```

There are 16 bytes per block and we have 6 blocks. If we format the message as we see in the server code, this means that the flag must be at least 25 bytes (if the last character of the message completes a block, the last block is filled with padding). The maximum flag size can be 24+15=39 bytes (filling up all but one byte of the last block so a new one is not added for padding). 

Let's try to figure out the exact flag size (this is not super necessary to do to solve). Basically, we just need to send more and more data until the encrypted output gets bigger by the size of on block (32 hex chars). For example, if looking at the previous "diagram", the flag took up all but the last byte of the 6th block, it would only take us adding a single character to our username to push the every other character 1 slot, moving the last flag byte to the last byte of the 6th block, requiring a new block of padding to be added, making out encrypted output larger by one block. 

Here is a quick script to do that:
```python
from pwn import remote, context
context.log_level = 'error'

def attempt(payload):
    p = remote("localhost", 8000)
    p.recvline()
    p.recvuntil(b"~> ")
    p.send(payload)
    p.recvline()
    p.recvline()
    p.recvline()
    p.recvline()
    enc = p.recvline().decode().strip()
    p.close()
    return enc

def get_flag_len():
    payload = "admin\n"
    min_len = len(attempt(payload.encode())) # this will give us that 192 hex char output we discussed before
    print(min_len)
    i = 1
    while True:
        payload += "A"
        length = len(attempt(payload.encode()))
        if length > min_len: # we finally pushed the flag enough to get a new block
            print(i) # this is the num of characters we had to add to push the flag enough spots
            print(length)
            break
        i += 1
get_flag_len()
```
Output: 
```console
$ python3 solve-ecb.py
192
16
224
```
We see that the `min_len` printed 192 as expected. Then we see that it took 16 bytes to get a new block, which we can verify by seeing that the new output length is 224 hex characters = 112 bytes of input = 7 blocks. If it took 16 characters to push the last character of the flag to the last slot of the 6th block, it means there must have been 0 flag characters in the 6th block (it must have been all padding, the last flag character was the 16th byte of the 5th block). This is then an accurate diagram of the flag, which must be the minimum length of 25 bytes:
```
|admin%, here is |
|your top secret |
|access code for |
|today: PCTF{????|   
|???????????????}|  
|XXXXXXXXXXXXXXXX|
```

Now, the idea to solve this is abuse the fact that every block in ECB mode is encrypted seperately, so two equal plaintext blocks will produce equal output. We just need to manipulate our input to make two identical plaintext blocks. Let's look at the following diagram:
```
|admin%0000000000|   0 = any filler character (0*10)
|?XXXXXXXXXXXXXXX|   ? = a guess character
|PPPPPPP, here is|   P for push (P*7)
| your top secret|
| access code for|
| today: PCTF{---|   
|----------------|
|}XXXXXXXXXXXXXXX|   X = \x0f (padding)
```

Look at the last block. It contains the last flag character with padding. Now look at the 2nd block. We have control of what we put here, so we can replace `?` with a character we want to guess and the remaining 15 bytes with correct padding. If we brute force every character, at some point the `?` will be a `}`, thus making 2nd and last blocks identical. The encrypted output will have matching blocks, telling us we guessed the right character. To get to this point, we need to fill the first row with a filler character so we can start putting stuff in the second row (our guess). Then, we will need 7 more characters to push the remaining message enough spots to push the last flag character over to a new block.

Once we have the first, we can check the second to last flag byte:
```
|admin%0000000000|
|?}XXXXXXXXXXXXXX|
|PPPPPPPP, here i|   P*8
|s your top secre|
|t access code fo|   
|r today: PCTF{--|    
|----------------|
|-}XXXXXXXXXXXXXX|   X = \x0e
```
Notice we want an extra push character to get the next flag byte into the last block.

Now we write out solution script:
```python
from pwn import remote, context
import string

context.log_level = 'error'

def attempt(payload):
    p = remote("localhost", 8000)
    p.recvline()
    p.recvuntil(b"~> ")
    p.send(payload)
    p.recvline()
    p.recvline()
    p.recvline()
    p.recvline()
    enc = p.recvline().decode().strip()
    p.close()
    return enc

flag_len = 25
guessed = ""
payload = "admin\n" 
payload += "0"*10 # fill remainder of first block

for _ in range(flag_len):
    for c in string.printable:
        # prepend current guess to already guessed
        # ex: ?}   if } already guessed and ? is current guess
        guess = c + guessed 
        cp = payload + guess # cp is our current payload

        # don't add padding when our guess is a full block
        if len(guess) % 16 != 0: 
            pad = 16 - (len(guess) % 16)
            cp += (chr(pad)*pad)

        # modulo len(guessed) by 16 to avoid a full block of push characters
        cp += 'P'*(len(guessed) % 16 + 7) 

        out = attempt(cp.encode())
        # compare the second and last blocks (2 and 7)
        # if equal, our guess is right
        if out[32*1:32*2] == out[32*7:32*8]:
            guessed = c + guessed
            print(guessed)
            break
```

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/solve-ecb.png" width=20%  height=20%></p>
