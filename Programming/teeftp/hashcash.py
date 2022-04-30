#!/usr/bin/env python3

import os
from hashlib import sha1
import base64

# Generating random numbers to help with bruteforcing
firstpart = base64.b64encode(os.urandom(16))
secondpart = base64.b64encode(os.urandom(4))

# Hash format
hash_ = sha1(b"1:20:220222:admin@patriotctf.com::"+firstpart+b":" + secondpart)

# Bruteforced here
while hash_.hexdigest()[:5] != "00000":
    firstpart = base64.b64encode(os.urandom(16))
    secondpart = base64.b64encode(os.urandom(4))
    str = b"1:20:220222:admin@patriotctf.com::"+firstpart+b":" + secondpart
    hash_ = sha1(str)

    print(hash_.hexdigest(), firstpart, secondpart, str)

# Prints out the required payload
print()
print("====================================================================")
print("Flag Payload = ", str.decode("utf-8"))
print("Sha1Sum = ", sha1(str).hexdigest())
print("====================================================================")

