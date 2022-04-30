# Flexi

### Description
Discover the flag within the .zip attachment

### Difficulty
Medium

### Flag
`PCTF{CL34rT3xt_N3v3r_F3lt_S0_Gud}`

### Hint
secretsdump is your friend

### Author

Matthew Morrow

### Writeup

Download the attached zip file. Extracting the contents will provide a ntds.dit and system hive file.  Use secretsdump.py to extract the password hashes, including a cleartext password that contains the flag.


/usr/share/doc/python3-impacket/examples/secretsdump.py -ntds ntds.dit -system system LOCAL



