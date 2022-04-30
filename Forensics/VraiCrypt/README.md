# WIP Vrai Crypt


### Description
One of our (ex) employee's was caught using some outdated disk encryption software called VraiCrypt or something like that. We managed to grab the encrypted disk file and a dump of the memory from their workstation. Can You extract the contents of the encrypted disk?

Note: Both this challenge and `update with new challenge name` use the same memory dump file to save your valuable hard drive space. 

### Difficulty
3/10

### Flag
`PCTF{r1P_7rU3CrPY7}`

### Hints
The program Volatility is commonly used to investigate memory dumps

### Author
Matthew Johnson (Meat Ball)

### Writeup
This challenge is a play on words of the now obsolete encryption software TrueCrypt.
To begin, use [Volatility](https://www.volatilityfoundation.org/) to identify some base information about the image using the imageinfo command. Running this command shows that it is most likely a windows 7 machine.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/writeup-images/VolatilityImageInfo.PNG?raw=true"></p>

From this point forwards, we will use `--profile=Win7SP1x64` to tell Volatility to treat it as a windows 7 dump.
Some research shows that Volatility has a plugin to extract the master key from memory for TrueCrypt instances. Executing this plugin with out memory dump we receive the raw master key.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/blob/main/writeup-images/VolatilityMasterKey.PNG?raw=true"></p>

From here, there are a couple ways of progressing. For this writeup I will show a method using [MKDecrypt](https://github.com/AmNe5iA/MKDecrypt) which is a program that is capable of decrypting a TrueCrypt volume with only a master key. Running the command below will mount the TrueCrypt volume onto the system.
`python3 MKDecrypt.py SecretBoi 616dba8467f706ba40793d700946fd1c85515c641a2c35c3fb37c195ae1f488465b960750fb87ce3e0629d3157d588ed955483bb857cd2e0ae96fcabb4d7297d`

Inside of the mounted volume is a file called `flag.txt` which contains the flag `pctf{r1P_7rU3CrPY7}`
