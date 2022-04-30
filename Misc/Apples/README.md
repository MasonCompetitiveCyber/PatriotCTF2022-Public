# Name
Apples

# Description
I found this executable file from an old coworker who really likes apples. I think it contains some data we need to access, but I don't know how to get to it. I think he mentioned using a tool called steghide at one point when I talked to him, but when I tried using it on the executable file, it didn't work. Do you think that you can help me out here?

# Difficulty
Beginner

# Flag
pctf{@pples\_tast3\_amaz\!ng666}

# Hints
None

# Author Name
Nihaal Prasad

# Writeup
When executing the binary file, the following text is printed out.

```
$ ./apples    
Please enter the password: 
```

If we use the `strings` command, we can easily figure out that the password is `apples`. The `strings` command also prints out a crap ton of base64 data.

```
[...]

tpjGc5ZsYUZySDXnzrqluj0GqMl1bW/Q8gOjXbn5YWGMZyOgP+FMbQ7qSbCpnuM8ZFfoDoHgmO5tlcqXXcASR1YfXPTpXdx/DvTt6ExDJPHGeRyPwp4TMMXXm406EnbqYV6PJHnVRcsumh//2Q==
apples_reward
Please enter the password: 
apples
You're right! The correct password was apples!
You deserve some apples as a reward!
Sorry, that password was wrong!!!
;*3$"
GCC: (Debian 11.2.0-16) 11.2.0
Scrt1.o
__abi_tag
crtstuff.c
__CTOR_LIST__
__DTOR_LIST__

[...]
```

If you run the binary and use the password `apples`, the base64 data will be printed out in a file called `apples_reward`. You can also obtain the base64 data by copying and pasting it from the strings command if you want.

```
$ ./apples      
Please enter the password: apples
You're right! The correct password was apples!
You deserve some apples as a reward!

$ ls
apples apples_reward
```

The file can be decoded using the following command, which outputs an image file.

```
cat apples_reward | base64 -d > decoded.jpg
```

If you use steghide and input the password that was found earlier, you should obtain the flag.
```
$ steghide extract -sf decoded.jpg           
Enter passphrase: 
wrote extracted data to "data.txt".

$ cat data.txt
pctf{@pples_tast3_amaz\!ng666}
```
