#!/usr/bin/env python3

# Data from the storage
data = 'df9a4a98e45dd8ba5394494ff3712dde832f2a963d737365726464413713e8897d8bd34eefa964877e5cc4621acdb43c1d85'

# Separator
n = 2

# Separates the bytes
bt = [data[i:i+n] for i in range(0, len(data), n)]

# Reverses the bytes in correct order of input
bt_rev = bt[::-1]

# Prints out the reversed bytes
new_rev = ' '.join(bt_rev)
print(new_rev)

# Decodes to characters
decoded = [chr(int(x,16)) for x in bt_rev]

decoded = ' '.join(decoded)

print(decoded)

# Here we can see that after decoding there is a word
# called Address = 
# So, it's reasonable to not decode the hex data after that back to characters
# Which gives us the ethereum contract address
# 962a2F83dE2D71f34f499453Bad85De4984a9aDF
