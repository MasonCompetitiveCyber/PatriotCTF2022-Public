# Cryptogod

NOTE: `server.py` is what is shared with players (fake flag), `cryptogod.py` is the real server w/ the flag

### Description
Do you think you're a cryptogod? Connect to `nc <IP> <PORT>` and prove yourself.

### Difficulty
Hard

### Flag
`PCTF{c0ngr4ts_y0u_h4v3_f0rg3d_y0ur_w4y_int0_th3_s3ct}`

### Hints
1. The code is implementing CBC-MAC
2. CBC-MAC can be forged

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This is a CBC-MAC forgery challenge. Here is the important parts of the server code:
```python
FLAG = "real_flag_is_defined_here"
KEY = get_random_bytes(16)
BS = AES.block_size
IV = b'\x00' * BS

def encrypt(username):
    if not isinstance(username, bytes): 
        username = username.encode()

    pt = pad(username, BS)
    tag = AES.new(KEY, AES.MODE_CBC, iv=IV).encrypt(pt)
    if len(tag) > 16:
        tag = tag[-16:]
    return tag.hex()

<snip>

MASTER_KEY = encrypt("cryptogodadministrator")
cryptogods = ["cryptogodadministrator"]


<snip>

# <below code is simplified version of server code for easier understanding>
if username in cryptogods:
    req.sendall(b'\n' + b'-' * 48 + b'\n\n')
    req.sendall(b"That username already belongs to a crypto god!\n")
    stop = True
elif encrypt(username) != MASTER_KEY:
    req.sendall(b'\n' + b'-' * 48 + b'\n\n')
    req.sendall(b"You are not a crypto god it seems...\n")
else:
    admit_new_cryptogod(username)
    req.sendall(b'\n' + b'-' * 48 + b'\n\n')
    req.sendall(FLAG.encode() + b"\n")
```

Basically, user input is being encrypted and compared to the encrypted text `"cryptogodadministrator"`. We cannot simply send in that text, it will tell us that username already exists, so we need to send differnet input that will encrypt to the same output.

If you look at the `encrypt()` function, it is using `AES.MODE_CBC`, but returning just the last 16 bytes and calling it a tag. The IV is also 0. This should be enough information to determine that this is an implementation of CBC-MAC, and a bad one at that. It is vulnerable to forgery. 

Here is the structure of CBC-MAC:
<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/CBC-MAC_structure_(en).svg/570px-CBC-MAC_structure_(en).svg.png" width=60%  height=60%></p>

If we know the MAC output and the original message that created that MAC, we can control the result of the any blocks we append to the original message. Let's look at this image:
<p align="center"><img src="https://jsur.in/82b9b44e48c8cb7bd3590f6079ccf80b/cbc-mac-attack.svg" width=60%  height=60%><br><em>https://jsur.in/posts/2020-04-13-dawgctf-2020-writeups</em></p>

If the orginal message is `n` blocks, and we append to that message one more block, then we know exactly what is being XOR'd: MAC of original message (T) ⊕ our new message of block-size 1 (m'). Let's say our `m' = T ⊕ original message block 1 (M1)`. This means the XOR becomes `T ⊕ T ⊕ M1 = 0 ⊕ M1 = M1`. We have now basically restarted the entire MAC calculation as it had begun (CBC-MAC generally has an IV of 0, so the first block goes through without being changed by an XOR). 

If we create a new message like so: `M + (T ⊕ M[1]) + M[2-n]`, where `M = original message, T = MAC(M), M[1] = first block of M, and M[2-n] = all remaining blocks of M`, we will end up with the exact same MAC as the message `M` by itself while providing a different message.

More reading:
- https://book.hacktricks.xyz/cryptography/cipher-block-chaining-cbc-mac-priv
- http://blog.cryptographyengineering.com/2013/02/why-i-hate-cbc-mac.html
- https://jsur.in/posts/2020-04-13-dawgctf-2020-writeups

Here is my solution script:
```python
from pwn import remote, context, xor
from Crypto.Util.Padding import pad

context.log_level = 'error'

p = remote("localhost", 8000)
mac = p.recvline().decode().strip()[-32:]
print(mac)

msg = "cryptogodadministrator"
b1 = msg[:16].encode() # first block
b2 = msg[16:].encode() # the rest
msg = pad(msg.encode(), 16)

#       msg + xor(MAC, first block of msg) + remaining blocks of msg
forge = msg + xor(bytes.fromhex(mac), b1) + b2

p.recvuntil(b"~> ")
p.send(forge)
p.recvline()
p.recvline()
p.recvline()
result = p.recvline()
print(result)
p.close()
```

You can see that we send a message created exactly how we talked about before. Let's run it:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/solve-cryptogod.png" width=40%  height=40%></p>
