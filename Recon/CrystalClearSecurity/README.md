# Crystal Clear Security - 1

We found out that Schaef Fertecher is working for Crystal Clear Security. We 
were able to get her picture. Can you find her social media?

### Difficulty 

2/10


### Flag

`PCTF{s3cur!y_3nc0D3D}`

### Author
Yojan (drMoscovium)


### Write up

Combine the name and search it in mastodon.social 

<img src="https://drmoscovium.net/screenshots/2022-04-02-1648876618.jpg">

Decode the base64 post and you get the flag.

<img src="https://drmoscovium.net/screenshots/2022-04-02-1648876859.jpg">



# Crystal Clear Security - 2

Good Job finding the social media! Now it's time to find the hidden information
in her profile.

### Difficulty
5/10


### Flag

`PCTF{7rUly_CryP7ed}`


### Author
Yojan (drMoscovium)

### Write up 

Follow the account to get access to hidden posts. Dropbox link provides a video.
There's a hidden volume inside the video, and the password is in the comments/reply

Using the password, one can open the video VeraCrypt and get access to the flag, 
and other information.


# Crystal Clear Security - 3

Now that you got insider information about the company, see if you can do something 
with it. 

### Difficulty

4/10

### Flag

`PCTF{N1c3_s0ci@l_3ngin33ring}`


### Write up

Inside the video there's user credentials, and they can use that to login to a 
website and get the final flag.


