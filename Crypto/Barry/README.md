# Barry

### Description
I have come across this gibberish and I am certain that it contains very valuable information. Can you decode it for me?

### Difficulty
Medium

### Flag
`PCTF{stillhaventseenthefullmoviebeginningtoend}`

### Hints
Substitution Cipher

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Here is the cihpertext:
```$$=-=->;#&+%,_(*#^[|>;$$$^$^!@(*>;..(*$^$$..?(>;[]$$%),_$$[|,_>;(*[|?:>=#&>=,_?((*>;..$$|}$$@%>=>=?(?:>;<!$^+%@%>=$$@%$^>=[|>;[]$^|},_[|?(..,_(*#^?($$#&>=[|>;>;?(:{$$$^$^[|>;#^>=[|,_[|?([]$$[|$^,_[|[|$^>=@%>;+%|}>;[][][|?:>=#^#&>;<!(*+%[|?:>=@%>=>=>;[]=->;<!#&?(>=[]$^,_>=?($$(*|}..$$|}@%>==-$$<!?(>=@%>=>=?(+%>;(*[|=-$$#&>=..?:$$[|?:<!:{$$(*?([|?:,_(*!@,_?(,_:{+_>;?(?(,_@%$^>=|}>=$^$^>;..@%$^$$=-!@|}>=$^$^>;..@%$^$$=-!@|}>=$^$^>;..@%$^$$=-!@|}>=$^$^>;..@%$^$$=-!@>;>;?:@%$^$$=-!@$$(*+%|}>=$^$^>;..$^>=[|?(?(?:$$!@>=,_[|<!+_$$$^,_[|[|$^>=@%$$#&#&|}@%#&>=$$!@[]$$?([|,_?(#&>=$$+%|}?:>=#&>=,_?([|?:>=[]$^$$#^?([|,_$^$^?:$$%)>=(*[|?(>=>=(*[|?:>=[]<!$^$^:{>;%),_>=@%>=#^,_(*(*,_(*#^[|>;>=(*+%```

This cipher is replacing one letter with two special characters. You can do frequency analysis on this to convince yourself that this must be right (https://www.dcode.fr/frequency-analysis).

Here is a quick script to convert every two special characters into some letter so we can use an online substitution solver online:
```python
import string

ciphertext = "$$=-=->;#&+%,_(*#^[|>;$$$^$^!@(*>;..(*$^$$..?(>;[]$$%),_$$[|,_>;(*[|?:>=#&>=,_?((*>;..$$|}$$@%>=>=?(?:>;<!$^+%@%>=$$@%$^>=[|>;[]$^|},_[|?(..,_(*#^?($$#&>=[|>;>;?(:{$$$^$^[|>;#^>=[|,_[|?([]$$[|$^,_[|[|$^>=@%>;+%|}>;[][][|?:>=#^#&>;<!(*+%[|?:>=@%>=>=>;[]=->;<!#&?(>=[]$^,_>=?($$(*|}..$$|}@%>==-$$<!?(>=@%>=>=?(+%>;(*[|=-$$#&>=..?:$$[|?:<!:{$$(*?([|?:,_(*!@,_?(,_:{+_>;?(?(,_@%$^>=|}>=$^$^>;..@%$^$$=-!@|}>=$^$^>;..@%$^$$=-!@|}>=$^$^>;..@%$^$$=-!@|}>=$^$^>;..@%$^$$=-!@>;>;?:@%$^$$=-!@$$(*+%|}>=$^$^>;..$^>=[|?(?(?:$$!@>=,_[|<!+_$$$^,_[|[|$^>=@%$$#&#&|}@%#&>=$$!@[]$$?([|,_?(#&>=$$+%|}?:>=#&>=,_?([|?:>=[]$^$$#^?([|,_$^$^?:$$%)>=(*[|?(>=>=(*[|?:>=[]<!$^$^:{>;%),_>=@%>=#^,_(*(*,_(*#^[|>;>=(*+%"

mapping = {}
chars = list(string.ascii_lowercase)
output = ""

for i in range(0, len(ciphertext), 2):
	bigram = ciphertext[i:i+2]
	if bigram not in mapping:
		mapping[bigram] = chars.pop()
	output += mapping[bigram] 

print(output)
```

Output:
```console
zyyxwvutsrxzqqptxotqzonxmzluzruxtrkjwjuntxozizhjjnkxgqvhjzhqjrxmqiurnoutsnzwjrxxnfzqqrxsjrurnmzrqurrqjhxvixmmrkjswxgtvrkjhjjxmyxgwnjmqujnztiozihjyzgnjhjjnvxtryzwjokzrkgfztnrkutpunufexnnuhqjijqqxohqzypijqqxohqzypijqqxohqzypijqqxohqzypxxkhqzypztvijqqxoqjrnnkzpjurgezqurrqjhzwwihwjzpmznrunwjzvikjwjunrkjmqzsnruqqkzljtrnjjtrkjmgqqfxlujhjsuttutsrxjtv
```

Now plug it in https://www.boxentriq.com/code-breaking/cryptogram to solve it:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/barry-solve.png" width=70%  height=70%></p>
