# No Postcode Envy

### Description
And we'll never be royals.... (royals)

### Difficulty
Beginner

### Flag
`PCTF{OHLORDE}`

### Hints
This is a type of barcode used in the UK.

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Here is the challenge image:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/Crypto/No%20Postcode%20Envy/message.png" width=40%  height=40%></p>

If you Google stuff about postcodes, you will find that they're used in the UK. You may find references to the Royal Mail Group as well. Searching `postcode barcode` or `royal mail barcode` will show you what looks exactly like our image. The challenge title is a song lyric from "Royals" by Lorde, which can help confirm Royal Mail Group as the right path. Here are the alphanumeric codes:

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Rm4scc.svg/800px-Rm4scc.svg.png" width=40%  height=40%></p>

After following the RM4SCC format and decoding the correct sections, you'll get the message: `OHLORDE`
