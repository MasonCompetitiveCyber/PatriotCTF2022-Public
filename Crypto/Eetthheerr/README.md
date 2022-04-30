# Eetthheerr

### Description
::::::::Part One:::::::

After a while, you wake up in a room next to a broken table, surrounded by big walls from all sides.
You have always been an explorer and recently discovered this old building; looking around it seems like it may be a library, but you see a blinking green light in the distance. 
As you approach the light you realize it is a blinking terminal with a ethereum keystore file that you created long time ago, encrypted with a password which you can't remember as of now.
Can you crack the password, and locate the super secret flag through one of the publicly available block explorers?
I believe you can! You Rock!

Flag Format: PCTF{}

### Difficulty 
Medium

Cracking might take about 5 minutes or more.

### Flag
PCTF{Precious_Rockyou_Leads_To_Free_Ether}

### Hints
John is always a good friend.

### Author
Biplav Gautam

### Tester
None yet

### Writeup
```
The given file is an encrypted ethereum keystore file generated using go-ethereum package.
The security of this keystore file is dependent on randomness of the password.
I used a simple password from rockyou.txt.

First, ethereum2john can be used to convert the given file to a hash format that can be easily cracked with hashcat using rockyou.txt wordlist.

Once the password is cracked, the next goal is to get the public address of the wallet.

It can be done in multiple ways:
- Metamask can be used to import the given wallet with the cracked password.
- Or with some lines of code, the public address of the wallet can be found.

Once public address is available, goerli testnet explorer can be used to look up that address, and all transactions will be listed there.
One of them will have the flag.
```

