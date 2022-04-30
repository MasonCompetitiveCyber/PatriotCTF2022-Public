# Name
BOF Warmup

# Description
Don't feel like doing a tough pwn challenge? Here's one that you should be able to get easily. If you're having trouble, do some research on buffer overflows in C.

TODO: Put a netcat command here telling them which server to connect to in order to test the exploit.

# Difficulty
0.5/10

# Flag
I haven't programmed a flag into this yet. Basically, after they exploit the program, they should get a shell into the server running this program. There should be a flag.txt file on that server in the same directory as the program, which they should be able to cat. Whoever is setting up this server can just put whatever they want into the flag.txt file and have that be the flag.

# Hints
None

# Author Name
Nihaal Prasad

# Writeup
When you run bof\_warmup, just send a bunch of characters to it, and it'll automatically give you a shell. Later, we should make sure to add a flag.txt file in the same directory as the binary so that people can just open it to get the flag.

```
$ ./bof_warmup
Enter your name: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Opening shell...
$ ls  
bof_warmup  bof_warmup.c
$ whoami
kali
$ 
```
