#!/usr/bin/python3

import socket

# Header size, data size, block size, and source port defined here
header_size = 4; data_size = 2048; loopCount = -1
block_size = header_size + data_size
source_port = 1337
remote_address = 'chal1.pctf.competitivecyber.club' 
remote_port = 69
# Socket is created
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('0.0.0.0', source_port))
client_socket.settimeout(2.0)

# Remote Address defined here
remoteaddr = (remote_address, remote_port)

# Packet with blksize header option
requestData = bytearray(b'\x00\x01flag.jpeg\x00octet\x00blksize\x002048\x00hashcash\x001:20:220222:admin@patriotctf.com::ELTMFfAaoKPmg78jeUD/YQ==:GA/iYQ==\x00')
#requestData = bytearray(b'\x00\x01flag.jpeg\x00octet\x00blksize\x002048\x00hashcash\x001:20:220222:admin@patriotctf.com::u0N0nq2kRHDQ7k7ydinRxg==:kDhU8w==\x00')

# Sends first packet
client_socket.sendto(requestData, remoteaddr)

# Response is saved here
(buffer, (host, port)) = client_socket.recvfrom(block_size)

# This is acknowledgement packet that will be sent later for received data
ack_pac = bytearray(b'\x00\x04')

# Used to store all of the bytes to write to a file later
toWrite = bytes()

print("Downloading file")

while True:
    try:
        # Crafting packet to send including acknowledgement
        loopCount += 1
        toSend = ack_pac + loopCount.to_bytes(2, 'big')

        # Sends the packet here
        client_socket.sendto(toSend, (host, port))

        # Receives the packet from server and stores to buffer
        (buffer, (host, port)) = client_socket.recvfrom(block_size)
        
        # Prints only header info
        print(buffer[:4])

        # Appending everything exccept buffer
        toWrite += buffer[4:]

    except:
        # Open file and writes bytes
        f = open('flag.jpeg', 'wb')
        f.write(toWrite)
        f.close()
        print("File Downloaded")
        exit(0)
