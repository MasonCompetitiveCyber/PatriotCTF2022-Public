# Session Spy

### Description

Our company's domain controller server was recently hacked. We suspect the attacker hacked into our sysadmin's laptop and then logged in through RDP to the server and created a backdoor user to use later. Provided is a snapshot of the sysadmins's user folder from his laptop. Can you figure out the user the attacker created on the domain controller?

Flag format: `PCTF{username}`

### Difficulty
Medium

### Flag

`PCTF{svc_admin}`

### Hints

It's a good thing we didn't clear the cache

### Author

Andy Smith

### Tester

### Writeup

RDP sessions store a bitmap cache by default in the `C:\Users\USERNAME\AppData\Local\Microsoft\Terminal Server Client\Cache` folder on the local computer (where the RDP connection originates). You can often find useful information in there about what somebody did when connected to a RDP session on a remote computer.

You're provided with a snapshot of a user's folder, which has previously connected to the domain controller via RDP. Because of this, there is a file in the Cache directory above called `Cache0000.bin`.

To extract the bitmap files from this cache, use this tool: https://github.com/ANSSI-FR/bmc-tools

Sample:

```
python .\bmc-tools.py -s Cache -d out -b
[+++] Processing a directory...
[===] 2936 tiles successfully extracted in the end.
[===] Successfully exported 2936 files.
[===] Successfully exported collage file.
```

The directory contains a lot of images, so to make it easier to spot the correct ones, the `-b` flag combines them into a collage, `Cache0000.bin_collage.bmp`.

This collage can be seen below:
![](/writeup-images/Cache0000.bin_collage.png)

If you zoom in at the center top, you can see a powershell window open that is running `net user svc_admin password123! /add`.

![](/writeup-images/Cache0000.bin_collage-zoomed.png)

The flag is the username `svc_admin`.
