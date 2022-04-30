# Foxi

### Description
Extract the saved password from the Mozilla Firefox roaming profile

### Difficulty
3/10

### Flag
`PCTF{Br0ws3rs_ar3_th3_b3st_P@ssw0rd_R3p0s}`


### Author

Matthew Morrow

### Hint 1
https://github.com/lclevy/firepwd

### Writeup

Download and extract foxi.zip file.  Expand the directory to the appdata\roaming\Mozilla\Firefox\Profiles\3y1wxf49.default-release folder.  You need the key4.db and logins.json in order to proceed.  

Next, use firepwd  to extract the credentials. -- https://github.com/lclevy/firepwd 

Point the script to the location of the key4.db and logins.json

python3 /tmp/firepwd/firepwd.py /tmp/appdata/roaming/Mozilla/Firefox/Profiles/3y1wxf49.default-release/

The password will be displayed

decrypting login/password pairs

   `http://pctf.local:b'ctfuser',b'PCTF{Br0ws3rs_ar3_th3_b3st_P@ssw0rd_R3p0s}'`
                        
Alternatively, you can put the logins.json and key4.db in an existing firefox roaming profile folder and then open the browser and navigate to settings --> saved logins and click the "eye" icon to reveal the cleartext password. 


