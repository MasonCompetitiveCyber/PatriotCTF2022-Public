# CaptSHA

### Description

This service requires some sort of captcha to access it. Can you get in?

Flag format: `PCTF{}`

### Difficulty

4/10?

### Flag

`PCTF{y0u_c4ptur3d_th3_c4ptcha}`

### Hints

### Author

Andy Smith

### Tester

### Setup

```bash
# Compile
go build -ldflags="-s -w" captsha.go

# Run
socat tcp-l:5000,reuseaddr,fork EXEC:"./captsha",pty,stderr,echo=0
```

### Writeup

The problem requires you to find SHA-1 hashes that end in two specific bytes. You send the service a string, it hashes it, and checks to see if the ends match. To make sure this isn't done by hand, each question must be done within 5 seconds.

An initial connection will look like this:

```
--------------------------------------------------------------
Welcome to the CaptSHA flag service!
To limit spam, we are now requiring a captcha to be completed.
To do this, we use a hashing proof-of-work system.
You must enter a string. We will hash it using SHA1.
The hash must end with the specified bytes.
You have 5 seconds for each of the 25 questions. Let's begin!
--------------------------------------------------------------
[Question 1] Please enter a string whose SHA1 hash ends with 340b:
```

When creating a script to solve this, the trick is to build a hash set before starting that contains of all the hashes that end in different two-byte sequences and a corresponding string for each. The simplest way to do this is to start a loop and just count up from zero, hashing the string of "0", "1", ..., and adding them to a hashmap / dictionary until all 65,536 possibilities are found. This should only take a second or two, or maximum a minute or two on slower hardware or a VM. Then connect to the challenge port and loop through each question and respond with the ending bytes in the dictionary.

An example solution script can be seen in `captsha_solution.py`.
