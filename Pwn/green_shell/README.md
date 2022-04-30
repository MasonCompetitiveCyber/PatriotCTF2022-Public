# Green Shell

# Description
- Shells are pretty hard body parts. Can you break out of this one?

# Difficulty
- 1

# Flag
- PCTF{U_no_wat_tH3y_say_@ll_to@sTers_toaST_T0@st}

# Hints
- Alright gang, let's see what's really handling all the commands we've been giving it!

# Author Name & Discord
- Brandon "Veryyes" Wong

# Challenge Tester

# Write Up
Disassembling this program will quickly reveal that the shell is reall just calling `/bin/bash -c` on input given. There are also three checks that **only** check the first value of the command inputted. Therefore we can push more than one shell command with `;` for example.

This will solve the challenge
`ls ; cat ../flag`