# Golf

### Description

Create the smallest (64 chars or less) C program possible that prints the output:

```plaintext
* * * * *
* * * * *
* * * * *
* * * * *
```

Four rows of five asterisks with a space between each (trailing whitespace is irrelevant as long as there's a newline).

The code should compile on a standard up-to-date Linux GCC install with no additional compiler flags (i.e. `gcc program.c -o program`) and must execute without any command line arguments.

Compiler warnings are fine, as long as the code runs.

The smallest known solution to us is 49 characters.

The scoring structure is as follows:

| Characters | Award                   |
| ---------- | ----------------------- |
| 56 to 64   | Flag                    |
| 51 to 55   | Flag + 25 bonus points |
| 49 to 50   | Flag + 50 bonus points |
| < 49       | Flag + 100 bonus points |

<br>

Final entries are due 1 hour before the end of the competition.

**Submit your code to Andy in Discord (not in the flag box!)**

### Difficulty

Medium

### Flag

`PCTF{n0w_pl4y_s0m3_c0d3_g0lf}`

### Author

Andy Smith

### Tester

### Writeup

**Bonus point amounts are still being decided**

I (Andy) will handle the manual scoring of these. The scoring table is listed above. The flag will be given out for all scoring entries less than the maximum character count, and additional bonus points will be awarded for smaller programs. Bonus points can be awarded in CTFd for a specific user on a team and will count towards the teams total score.

#### Scoring

Compile the program with `gcc prog.c -o prog`

Calculate character count with `cat prog.c | sed -z '$ s/\n$//' | wc -c`

Smallest solution from the CTF is the following, 39 characters:

```c
main(i){for(;++i<6;)puts("* * * * *");}
```
