# RoboTron9000

### Description

My AI has gone rogue and hard coded its health, so we can't edit it down.
It seems to have gotten quite arrogant and believes itself to be invincible.
Could you manipulate the running program's memory to show RoboTron9000 otherwise please?

Flag Format: PCTF{}

### Difficulty
3 (Very Easy)

### Flag
PCTF{8yp455_h42d_c0d3d_v41u35}

### Hints
None

### Author
Migyaksuil (Maxime Bonnaud)

### Tester
None yet

### Writeup
```
To begin, we can disassemble the binary in Ghidra and get an idea of what the code is doing. From there we see that the value is indeed hardcoded at 1000 (this is also explicitly said by RoboTron9000 when the binary is ran). Using this information, we can rule out trying to reverse engineer a passphrase or trying an attack on the buffer.
As the challenge instructions imply, our goal is to find the memory address holding the health value and manipulate it to pass the health check and get our flag.
Since we know the value to be 1000, a scan for a 4 byte, exact value integer yields only one memory address.
From there, you can write a program or if the scanning program supports it, just change the value directly.
The best time to change the value is when the program is still waiting for input.
After changing the health value (to 0 or less), input anything (user input is irrelevant) and we get the flag.

```

Here's what that looks like visually:

First we disassemble it in Ghidra and see that user input does nothing and that the main bypass must happen by changing the health value to pass the check and get the flag:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/ghidra_view.png" width=60%  height=60%></p>

Next, we run the process and attach a memory scanner to the process (I used Cheat Engine, but alternatives like Squalr, scanmem, and PINCE exist).

Then, we scan for a value of 1000 (4-byte and non-hex) and see two values (sometimes just one):
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/first_scan.png" width=60%  height=60%></p>

To confirm which address is the correct one, we double-click on both (adding them to the memory manager), then right click on either one and select [find out what accesses this address]:
One of them (0060FF14 in this instance) will show this:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/access_instr.png" width=40%  height=40%></p>

The most interesting instruction is the cmp dword ptr [esp + 44], 00

In English, this means that the value held in esp (0060FED0) + 44 = (0060FF14) is being compared with 0. This is the check we need to bypass and confirms that this is the right address.

Now all we need to do is change the value to 0, and we get the flag after entering our user value.
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/result.png" width=60%  height=60%></p>

And there's the flag
