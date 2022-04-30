# Name
TeeFtp

# Description
Some weeks earlier I got chance to learn about Hashcash and Tftp. I thought of
creating a tftp server to securely share files with my friends. But, tftp doesn't
allow any sort of authentication. So, I asked my 1337 friend if I could implement 
some sort of validation. He suggested me to use hashcash, but I wanted it be to be 
ultra secure. So, I went ahead and read all the RFCs related to TFTP and stored
a secret flag in the server.

Unfortunately, due to some reasons I couldn't find any tftp client that lets me
download files from such a highly secured environment.

Can you craft 1337 packets and send them to the server and help me extract the secret file?
I promise to reward you with the flag.

Crafting a packet with follwing info will get you the flag:  
=> Send a Read request for file "flag.jpeg" on octet mode  
=> Blocksize should be 2048  
=> Additional custom tftp option "hashcash" should be included whose value  
    should be in the X-Hashcash format:  
    ver:bits:date:resource:ext:rand:counter  
    where, ver = 1, bits = 20, date = 220222, resource = admin@patriotctf.com  
=> Since we all are 1337, source port also needs to be 1337.  


# Regarding Deployment
Tftpy can be installed with
`pip install tftpy`

I changed the server config by editing files in "/usr/local/lib/python3.8/dist-packages/tftpy"
which are included here.

Flag is inside `Flag` directory as `flag.jpeg`.


# Difficulty
7/10 ?

# Flag
Flag will be in the image file "flag.jpeg"

# Hints
RFC 1350, RFC 2347, RFC 2348, RFC 2349 => Especially "OPTIONS" feature

# Author
Biplav

# Tester
None

# Writeup
This is a challenge where tftp protocol and its features are tested.

Tftp is a simple protocol that doesn't support any authentication but we can add
extra option information in header as defined in RFC 2347.

If a client sends a request to read file with additional options, the server sends
OACK response.

Then, client sends ACK response with block number 0, after that real data
transmission happens where server sends DATA, 1, client sends back ACK, 1 and so on.

I added several checks in the server such as the source port of the client should be
1337, blocksize option must be 2048, and also added a custom hashcash header option 
whose SHA-1 hash value must have 5 leading zeroes.

When all of those are combined to create a packet, the server will send the flag back 
where client needs to handle properly to get all of the bytes back.

Example request can be something like this:
```
\x00\x01flag.jpeg\x00octet\x00blksize\x002048\x00hashcash\x001:24:220222:admin@patriotctf.com::UnWBVlFW8H5fqqVjqkKznA==:neiNt/KKQE8=\x00
```

Full code for client is included in `client.py` file.  

Also, the code to generate hashcash header is included in `hashcash.py`

