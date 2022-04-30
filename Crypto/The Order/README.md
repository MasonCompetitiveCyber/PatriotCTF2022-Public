# The Order

### Description
We are not sure what these strange characters are supposed to mean. Can you decipher it?

### Difficulty
Beginner

### Flag
`PCTF{Dop3_numb3r_syst3m!}`

### Hints
An Order of monks used this.

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Here is the cipher image:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/Crypto/The%20Order/cipher.png" width=40%  height=40%></p>

After some reverse image searches and Googling, you may stumble upon the Cistercian number system that looks like this:

<p align="center"><img src="https://www.zmescience.com/mrf4u/statics/i/ps/cdn.zmescience.com/wp-content/uploads/2021/01/cistercian_numbers.jpg?width=1200&enable=upscale" width=40%  height=40%></p>

Now we must get the decimal values of each numeral, they should come out to: `6811 1112 5195 1101 1710 9985 1114 9511 5121 1151 1651 1093 3`. Let's plug this into a decimal to ascii converter (such as https://onlineasciitools.com/convert-decimal-to-ascii) after removing the spaces. You should get the following message: `Dop3_numb3r_syst3m!`