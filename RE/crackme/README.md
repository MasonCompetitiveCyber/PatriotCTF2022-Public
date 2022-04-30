# Name
Crackme

# Description
This program is password protected, and I can't figure out how to crack it! Can you help me out here?

# Difficulty
2/10

# Flag
pctf{YoU\_hav3\_Cr@cked\_Me!6789}

# Hints
None

# Author Name
Nihaal Prasad

# Writeup
The hardest part about this binary is reading the code and figuring out what it's actually doing. Once you figure out how it works, all you have to do to solve this binary is go backwards. Basically, when you type in the password into the program, it will first base64 encode it. Then, it will add 20 to each character, and if the result isn't a printable ASCII character, it goes to the start of the printable ASCII table (basically acting like a shift 20 Caesar cipher that includes every ASCII character). Finally, a function is called that checks whether the final output is equal to ```9{$d0DJ08e,<7{zf#emx9Av@7f,A.deB}*/g%xBmw=qq```.

So to solve the binary, do the following:
1. Shift each character in ```9{$d0DJ08e,<7{zf#emx9Av@7f,A.deB}*/g\%xBmw=qq``` backwards by 20.
2. Base64 decode the result to get the flag.
