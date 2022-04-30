# Name
OverComplicated

# Description
I sure do like making things more complicated that they need to be.

# Difficulty
Easy

# Flag
pctf{s0meT1me$\_YoU\_g0TtA\_dO\_iT\_loNG\_h4Nd}

# Hints
None

# Author Name
Robert Weiner

# Author Note
Only distribute OverComplicated.rar to the players

# Writeup
The flag is simply XORed 4 times, by 0x50 (P), 0x43 (C), 0x54 (T), and 0x46 (F). Each XOR is done with a different construction of the XOR logic gate: 0x50 is NAND construction (BoOp), 0x43 is NOR (OopiDy), 0x54 is NOT/OR/AND (ShoOp), and 0x46 is regular XOR (DoOp).
