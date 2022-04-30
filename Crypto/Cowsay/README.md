# Cowsay

### Description
I encrypted this file by XOR'ing it with my secret flag, but I seem to forgotten it. Please figure out the XOR key, I really need this file back!

Reminder: flag format is PCTF{s4mpl3_fl4g}

### Difficulty
Easy

### Flag
`PCTF{this_is_4_sup3r_imp0rt4nt_bin4ry}`

### Hints
1. google xortool online

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Run xortool on the file:
```console
$ xortool xord_file                                                                              
The most probable key lengths:
 2:  12.0%
 4:  11.2%
 6:  10.2%
 8:   9.3%
10:   9.1%
12:   7.9%
14:   7.1%
16:   6.6%
19:  14.5%
38:  12.2%
Key-length can be 4*n
Most possible char is needed to guess the key!
```

Let's try length 19 first. The most common char is 0x20 in text files and 0x00 in binary data. We can try 0x20 first:
```console
$ xortool xord_file  -l 19 -c 00                                                                    1 ⨯
2 possible key(s) of length 19:
rCTF{thts_ts_4_sry3
rCiF{thts_ts_4_sry3
Found 0 plaintexts with 95%+ valid characters
```

Close, but that's definitely not a long enough key. Let's try length 38:
```console
# xortool xord_file -l 38 -c 20
1 possible key(s) of length 38:
PCTF{this_is_4_sup3r_i(p0rt4nt_bin4ry}
Found 1 plaintexts with 95%+ valid characters
```

Sweet. If you want to decrypt the file, you can use https://github.com/hellman/xortool/blob/master/xortool/tool_xor.py:
`$ tool_xor.py -f xord_file -s "PCTF{this_is_4_sup3r_imp0rt4nt_bin4ry}"`. You'll get the ruby script for cowsay.


Another way to solve is `apt install cowsay`, then `$ tool_xor.py -f xord_file -f /usr/games/cowsay` and it will spit out the flag. 