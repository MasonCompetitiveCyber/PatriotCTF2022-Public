# name
Cool VM 1
# description
I found this flag checker program, but it only runs on the cool VM
# difficulty
Expert
# flag
pctf{vms_are_pretty_cool}
# hints
none
# author name
caffix @caffix
# tester
chris issing (@thisusernameistaken)
# writeup
It's VM reverseing. You've got to figure out how the VM interprets .cool files and then
you need to either translate a .cool file into psuedo asm to reverse it, or break out
some gdb skills and watch when it perform the main key buffer comparisions.

The actual comparision part is just another XOR with a magic value of 11, they could
statically take it out once they've decoded the program and then manually XOR the value.
But it's not going to dump out with strings or anything too easy
