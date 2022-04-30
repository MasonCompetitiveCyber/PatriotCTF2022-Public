# name
Is it a stack
# description
My stack data structure in this program is acting weird can you help me?
# difficulty
4/10
# flag
pctf{N0_1ts_@_l1nk3d_l1st}
# hints
none
# author name
caffix @caffix
# writeup
Two ways to solve it, you can side-channel it by watching the RAX register after the XOR comparision and look for a 0 value.

But the real way I'm intending here is to figure out that it is a linked list data structure and the actual key-buffer comparision
is pretty much just an XOR. No rocket science here. Pretty standard crack-me stuff.
If you're in Ghidra/IDA/binja/r2 just start labeling all your variable pieces and maybe break out the data structure builder.

Decompiler will look much nicer once you've labeled head and tail nodes in the linked list and ghidra will pretty much show
you how it's reading the "key" buffer.

I bet if you're good enough at angr you could finagle an angr solve, but atleast out of the box is won't dump a flag for you since
I had it do an iterative counter for a checker instead of something like a memcmp or strcmp.
