# Delayed Start


### Description
An employee on our network messaged IT saying they found a flash drive in the parking lot. Before we could stop them, they inserted the drive and saw a command prompt briefly flash onto their screen. We managed to remotely dump the memory of their machine but are having trouble locating the program. Can you find the program and figure out what it does?

The flag is the number of seconds the program stays dormant for. For example, if the program wait 1 minute, the flag would be PCTF{60}.

Note: This challenge and Vrai Crypt use the same memory dump.

### Difficulty
Medium

### Flag
`PCTF{300}`

### Hints
The program Volatility is commonly used to investigate memory dumps
The virus may be disquised as something Totally Innocent

### Author
Matthew Johnson (Meat Ball)

### Writeup
This challenge is a play on words of the now obsolete encryption software TrueCrypt.
To begin, use [Volatility](https://www.volatilityfoundation.org/) to identify some base information about the image using the imageinfo command. Running this command shows that it is most likely a windows 7 machine.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/writeup-images/VolatilityImageInfo.PNG?raw=true"></p>

From this point forwards, we will use `--profile=Win7SP1x64` to tell Volatility to treat it as a windows 7 dump.
