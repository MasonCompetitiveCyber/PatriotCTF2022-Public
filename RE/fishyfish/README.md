# Name
fishyfish

# Description
This weird dude at work loves fish. He was fired for it. We found a weird assembly file on his machine when cleaning up his computer, can you figure it out?

# Difficulty
Hard

# Flag
pctf{f1Sh1ng\_4\_Y4te5\_b4t3s\_oR\_h34venLy\_G4t35}

# Hints
https://www.zeuthen.desy.de/dv/documentation/unixguide/infohtml/gdb/Dump_002fRestore-Files.html - small hint cost (hint is just the URL, to inform them that they need to dump a memory region to disk to solve, and this is the correct command doc page to do that in GDB)

# Author Name
Robert Weiner

# Author Note
Only distribute fishyfish.s to the players

# Tester
Chris Issing

# Writeup
  You're given an AT&T syntax assembly file. If you can't read assembly/AT&T syntax, you can always finish its compilation with GCC (as shown by the `GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0` string in `.LFE6`, command is `gcc -c fishyfish.s -o fishyfish`) and then toss it in your favorite decompiler. Once you have it in a format you understand, you can see it's all just the main function, and in it a socket is opened to <ip> <port>, and the `)$#5#f\"4'!)( /5.` string (`.LC0`) is XOR'd with 0x46. Then, the XOR'd string (`obese dragonfish`) is sent over the socket. This is the password the program uses to authenticate with the remote server, at which point the remote server will send back 0x3888 bytes, which is then written to a memory file descriptor named "fishchecker", and then the contents of that memfd are executed with fexecve() with no arguments.
  
  At this point, we need to extract the new in-memory binary. This can be done a variety of ways, but the easiest I know of is to break the program with GDB and dump the binary to disk with the `dump` command (https://www.zeuthen.desy.de/dv/documentation/unixguide/infohtml/gdb/Dump_002fRestore-Files.html). Alternatively, you can use netcat to directly pull the binary from the server with the following command: `echo -e '\x6f\x62\x65\x73\x65\x20\x64\x72\x61\x67\x6f\x6e\x66\x69\x73\x68' | nc host port > fishchecker 2>&1`. Upon decompiling this binary, we can see that it opens a file named `FISH_BAIT` and reads 0x2D bytes. The PRNG is set with the call `srand(0xDEFEC8ED)`, and then the checking algorithm begins. Each character read from `FISH_BAIT` is checked one at a time. This check consists of passing the input character to the `shuffle` function, then XORing it with 0x2A. All that's left now to get the flag is to determine what `shuffle()` does. (yes I know the symbols are stripped, but it's the only function the character is passed to in there so you know which one I mean).
  
  The `shuffle()` function takes in a char pointer and modifies it by reference. It will iterate over every bit in the char, and swap it with a random other bit. The bits can be swapped multiple times (I really didn't pay attention to how thoroughly it was shuffled lmao), but that doesn't matter as we know what `rand` was seeded with. We can use this information to build the swap index sequence, then just XOR the character array the input is being compared to with 0x2A and iterate through the swap sequence in reverse order across the array in reverse order. And with a little hand-waving at how annoying that is to do, we have the flag!
