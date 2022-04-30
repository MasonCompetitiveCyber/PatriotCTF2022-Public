# Spongebob

Note: provide main.php in challenge

### Description
Spongebob 😍

Flag format note: case insensitive

### Difficulty
2/10

### Flag
`PCTF{spongebob_looking_thicc}`

### Hints

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Setup
```
cd Spongebob
sudo docker-compose build
sudo docker-compose up -d
```

### Writeup

This is simple PHP command injection. There's one extra step in needing to escape out of the quotes from this line taking our input:
`$command = "python3.9 memetext.py \"$text\"";`

Here is a simple payload: `";ls;"`

The `ls` will reveal a flag image file you can then access.
