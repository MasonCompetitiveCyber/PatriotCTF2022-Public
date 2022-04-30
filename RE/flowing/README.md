# Name
flowing

# Description
Crashing on the rocks. Like water in a river. It can crash over.

# Difficulty
Easy

# Flag
pctf{Wh3rEf0R3\_Art\_Th0u\_0v3rFlOw}

# Hints
None

# Author Name
Robert Weiner

# Author Note
Only distribute flowing and inbytes to players

# Writeup
The only input taken from the user is a seed number which will be constrained to mod(65535). This seed will be used to generate a sequence of numbers mod(65535) which are offsets within the inbytes file to be read. Correctly guessing the seed value will result in the flag being printed to the screen. As there is only a seed range of 65535 numbers, this can be easily brute-forced, which is the most key discovery. A simple shell or angr script can solve this at this point by re-running the program with every number in the range, and checking if the output starts with pctf{
