# Name
Locked

# Description
My website has been completely locked down!!! I don't care how good of a hacker you are, you won't be able to hack my website!!!

TODO: Put the URL of the website.

# Difficulty
Easy

# Flag
pctf{Th3\_W3bsite\_w@s\_UnL0cK3d}

# Hints
None

# Author Name
Nihaal Prasad

# Writeup
You can brute force the website with dirbuster or something in order to figure out that there is a /admin directory. When you go look at the index.html file in this directory, you'll see it reference main.js. If you look at main.js, you'll see that there is a hidden page called ```secret```. While there is no hyperlink to the secret webpage, you can navigate to it by going to `http://URL/admin/#secret`. This will show a link to ```https://pastebin.com/F21q9Eu8 ```, and if you navigate to the link, the flag will appear.
