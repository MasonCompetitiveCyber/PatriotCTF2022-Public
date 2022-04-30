# Fly

### Description
We've found this very strange image and believe that it may be some sort of secret message. Can you decipher it?

### Difficulty
Hard

### Flag
`PCTF{glide_typing_is_honestly_the_bomb!}`

### Hints
Gboard

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Here is the cipher image:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/Crypto/Fly/cipher.png" width=40%  height=40%></p>

These series of images are traces of a google keyboard when using the "glide typing" method (called "swipe typing" on iphones) of typing on a smartphone keyboard. To solve this, just overlay each image over a google keyboard and figure out the word that must have been spelled with that trace. Let's start with a screenshot of the first image in the cipher.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/glide.png" width=40%  height=40%></p>

We can make the white background transparent with https://onlinepngtools.com/create-transparent-png:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/transparent.png" width=60%  height=60%></p>

Now let's get an image of an android google keyboard, like this one:

<p align="center"><img src="https://cdn.wccftech.com/wp-content/uploads/2016/12/Google-Gboard-Keyboard-app.jpg" width=30%  height=30%></p>

Finally, let's overlay the trace over the image of the keyboard. I'm sure you can do this with other applications, but I used Paint 3D. It's easy to line up with the border already given around each trace image.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/glide_overlay.png" width=40%  height=40%></p>

We can see that there are really only 2 possible words traced: `edilg` and `glide`. It's obvious which one it is. Now we just do the same with all the other images. The only different thing you must do are with the images of 2 dots. Those are special characters. Here is what it looks like overlayed:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/underscore_overlay.png" width=40%  height=40%></p>

We see a dot on the `?123` and in-between the `d` and `f`. If we look at the gboard special characters (which is what you get after pressing `?123`), we see that the underscore (`_`) lands basically in-between the `d` and `f`. 

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/gboard_special.png" width=30%  height=30%></p>

Do the same thing with the very last image and you'll get an exclamation mark (`!`).

After doing all of this you should get the message `glide_typing_is_honestly_the_bomb!`
