# Big Shaq

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/Programming/Big%20Shaq/INSTALL.md)

### Description
Are you on Big Shaq's math level? Solve 5 questions before the time runs out to see if you're worthy.

Connect with `nc <IP> <PORT>

### Difficulty
4/10?

### Flag
`PCTF{2_plus_2_1s_4_m1nus_0n3_th4ts_3_qu1ck_m4ths}`

### Hints
1. You can solve system of linear equations with Sympy

### Author
Daniel Getter (NihilistPenguin)

### Tester
UnicodeSnowmanDev (Matthew Johnson) ✔️

### Writeup

When you connect, you see something like this:
```console
$ nc localhost 8000
Question 1:
📙 + 🛐 + 🈲 + 🐽 + 📙 = -178
🐽 + 🈲 + 🈲 + 🕔 + 🐽 = -274
🈲 + 📙 + 🐽 + 🐽 + 🕔 = -227
🕔 + 🛐 + 🕔 + 📙 + 🐽 = -139
🛐 + 🛐 + 🕔 + 🐽 + 🕔 = -142

📙 + 🐽 + 🈲 + 🕔 + 🛐 =
```
You have 5 seconds to give the correct answer before it quits. [solve.py](solve.py) is my garbage solution script written on very little sleep, so do not judge. I am sure there are many better ways to do it.

Running it:
```console
$ python3 solve.py
52
b'Correct!\n'
116
b'Correct!\n'
-134
b'Correct!\n'
-201
b'Correct!\n'
115
b'Correct!\n'
b'PCTF{2_plus_2_1s_4_m1nus_0n3_th4ts_3_qu1ck_m4ths}\n'
```
