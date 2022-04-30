# CaptSHA SOLUTION
# PatriotCTF 2022
# Author: Andy Smith
# Category: Programming

from pwn import *
import socket
import hashlib
import time

IP_ADDRESS = "192.168.32.136"
PORT = 5000

# Create hash storage map of requested hash to our plaintext, e.g. "4af3" => "287334"
hashes: dict[str, str] = {}

# Number of hash possibilities (2 bytes)
POSSIBILITIES = 256 * 256

i = 0
# Loop through all possible combinations of bytes we might be asked for
while len(hashes) < POSSIBILITIES:
    # Generate a SHA1 hash of i
    hash = hashlib.sha1(str(i).encode('ascii')).hexdigest()
    # Add the hash to the dictionary
    hashes[hash[-4:]] = str(i)
    i += 1

    # Print progress every so often
    if i % 100 == 0:
        print(f"{len(hashes)*100/POSSIBILITIES:.2f}% {len(hashes)}")


# pwntools approach

# Connect to the remote server
conn = remote(IP_ADDRESS, PORT)

for _ in range(8):
    # Skip over the instructions text
    print(conn.recvline().decode(), end="")

# Loop over each question
while True:
    # [Question X] Please enter a string whose SHA1 hash ends with XXXX:
    question = conn.recvuntil(b": ")

    # Get just the requested ending 4 hash digits
    requested_hash = question[-6:-2].decode()

    try:
        # Look up the hash in our generated list
        response_hash = hashes[requested_hash].encode()
    except KeyError:
        # If the hash wasn't found, that likely means we got the flag
        print(question.decode(), end="")
        print(conn.recvline().decode())
        break

    # Send the response
    conn.send(response_hash + b'\n')
    print((question + response_hash).decode())

    # Your string's hash is: XXXX
    print(conn.recvline().decode())

conn.close()


# socket approach

# # Connect to the remote server
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((IP_ADDRESS, PORT))

# # Loop though each question
# while True:
#     # [Question X] Please enter a string whose SHA1 hash ends with XXXX:
#     question = s.recv(1024)

#     # Get just the requested ending 4 hash digits
#     requested_hash = question[-6:-2].decode()

#     try:
#         # Look up the hash in our generated list
#         response_hash = hashes[requested_hash].encode()
#     except KeyError:
#         # If the hash wasn't found, that likely means we got the flag
#         print(question.decode())
#         break

#     # Send the response
#     s.sendall(response_hash + b'\n')
#     print((question + response_hash).decode())

# s.close()
