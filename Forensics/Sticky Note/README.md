# Sticky Note

### Description

Steve is your typical boomer and stores his password on a sticky note on his monitor. Unfortunately, it has disappeared and he is locked out of his computer. He says he took a picture of the sticky note as a backup and saved it to his computer, but it appears to be deleted now. Can you recover his password for him?

Flag format: `PCTF{}`

### Difficulty

3-4/10?

### Flag

`PCTF{cant_h4ck_a_st1cky_n0te}`

### Hints

It's a good thing we didn't clear the cache

### Author

Andy Smith

### Tester

### Writeup

The picture previously existed in the Pictures folder, but it was deleted. However, Windows still stores the thumbnail for the image in the thumnail cache. These are located in `AppData\Local\Microsoft\Windows\Explorer\`

The `thumbcache_1024.db` and `thumbcache_1600.db` both contain a thumbnail of the image.

You can use a tool like [Thumbcache Viewer](http://thumbcacheviewer.github.io/) to open these files:
![](/writeup-images/stickynote1.png)

The full image can be seen below:
![](/writeup-images/stickynote2.jpg)
