#!/usr/bin/env python3
with open('opcodes','r') as f:
    lines = f.readlines()
for line in lines:
    if 'PUSH' in line and '0x' not in line:
        line = line.replace('\t',' 0x')
    with open('fixed_opcodes','a') as g:
        g.write(line)
