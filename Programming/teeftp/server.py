#!/usr/bin/python3

import tftpy

print("Server Started on port 69")

server = tftpy.TftpServer('./Flag')
server.listen('0.0.0.0', 69)

