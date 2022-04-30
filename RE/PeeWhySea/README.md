# PeeWhySea

### Description
Provide the right argument and you will have the flag.

### Difficulty
Beginner

### Flag
PCTF{t4k3_4_pyc}

### Hints

### Author Name
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This is just compiled python code, so we just need to decompile it. I used the tool [pycdc](https://github.com/zrax/pycdc). Easy install with `snap install pycdc`.

```console
$ /snap/bin/pycdc flag-checker.pyc         
# Source Generated with Decompyle++
# File: flag-checker.pyc (Python 3.9)

import sys
if len(sys.argv) != 2:
    print('One argument required')
    sys.exit()
arg = sys.argv[1]
key = 'ABCDEFGHIJKLMNOP'
encode = ''.join((lambda .0: [ '{:02x}'.format(ord(a) ^ ord(b)) for a, b in .0 ])(zip(arg, key)))
if encode == '110117023e3273237a157f133d372c2d':
    print('You have the correct flag!')
else:
    print('Wrong flag')
```

Briefly looking over it you can see it's XORing our input with `ABCDEFGHIJKLMNOP` and checking against hex `110117023e3273237a157f133d372c2d`. To get the flag, we just XOR `ABCDEFGHIJKLMNOP` with hex `110117023e3273237a157f133d372c2d`.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/pyc-solve.png" width=40%  height=40%></p>

Note: the decompiled code has this weird `lambda` and `.0` stuff, but that shouldn't really hinder finding the solution
