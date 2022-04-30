# Bézier

### Description
We are doing some DFIR on an employee's laptop after he got hacked. We've gotten everything except the method the hacker used to keep persistence on the machine. Luckily, we had backed up the employee's registry a few days before the attack. Given that registry file and one from after the attack, can you figure out the method of persistence used? 

The flag is the MITRE ID of the persistence mechanism. For example, the MITRE ID of "Scheduled Task/Job: Cron" is T1053.003, so its respective flag would be PCTF{T1053.003}

### Difficulty
Beginner

### Flag
`PCTF{T1546.002}`

### Hints
diff

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Basically, we just need to find the difference in the two registry files in the zip folder. The easiest way to do this is with the built-in linux tool `diff`.  

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/screensaver.png" width=40%  height=40%></p>

We see `SCRNSAVE.EXE"="C:\\Users\\Daniel\\Desktop\\shell.exe`, which looks sketchy. In Microsoft [docs](https://docs.microsoft.com/en-us/windows/win32/devnotes/scrnsave-exe), we see that this registry key "specifies the name of the screen saver executable file". Given that this executable is named "shell.exe", we can infer this is the method of persistence used by the hacker.

Now you just have to google `MITRE Screensaver Persistence` and you'll get it.