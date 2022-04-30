# mcchttp

# Description
- Flask? Django? Express.js? Ruby on Rails?? All are overrated. A REAL programmer should write it all in C.

# Difficulty
- 7 I think?

# Flag
- PCTF{wai_1s_my_CoDE_borkken}

# Hints
- `curl` and `wget` are on the machine

# Author Name & Discord
- Brandon "Veryyes" Wong

# Challenge Tester

# Write Up

mcchttp is a very crappy written HTTP server in C. The concept idea of the challenge was to give contestants a problem that tests both Vulnerability Research, Reverse Engineering and Pwning skills.


<!-- Not sure if tester should do the write up or the creator -->

<!-- ## Finding the Overflow

Since the problem claims the binary is an HTTP server and you can connect to `/` with a browser, clearly it talks HTTP on an exposed socket. And because it is a PWN challenge, we can rule out common web based attacks like a directory traversal or XSS.

With attacking network protocols we want to start taking apart the components within the protocol. an HTTP Request is comprised of:

**Request Line**
Space `0x20` delimited string ending in `\r\n` consisting of the following:

- HTTP Method String
- URI String
- HTTP Version String

**Headers**
An optional part of the protocol. Each header field is a key value seperated by a colon `:` followed by a space `0x20` and ends in a `\r\n`, like such:

```
Host: localhost
Server: Apache Webserver
```
This entire section is ended with another `\r\n` -->