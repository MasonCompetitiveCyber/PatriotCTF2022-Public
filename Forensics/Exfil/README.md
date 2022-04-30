# Exfil

### Description
Someone broke into our systems and managed to exfiltrate some data, but we don't know how. Can you find out what data they stole?

### Difficulty
Hard

### Flag
`PCTF{n0t_4_v3ry_sn34ky_3xf1l}`

### Hints


### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

The data was exfil'd in the data section of ICMP packets. If you open the pcap in wireshark and filter by `data`, you'll se this:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/data_filter.png" width=40%  height=40%></p>

The `no response found` packets are not normal and are a bit sus. Click on one and you'll see data that looks like this:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/ping_data.png" width=40%  height=40%></p>

We see data in the form `data:1:39:some-hex`. If you click through them, you'll notice that the first section is either `data` or `checksum`. `data` means data is being sent and `checksum` means it's the last exfil packet with the checksum of the entire data. The 2nd section is just the sequence number of the exfil packet and the 3rd section is the total number of data packets. 

Here's a quick script to scrape out the data:
```python
from scapy.all import *
import binascii

last_seqn = 0
result = ""

def get_payload(x):
	global last_seqn
	global result 
	
	try:
		load = x.load.decode()
	except:
		return
	
	split = load.split(":")
	exfil = split[0]
	if (exfil == 'data' or exfil == 'checksum'):
		seqn = int(split[1])
		total = int(split[2])
		data = split[3] 

		if(exfil == "checksum"):
			outf = open('out',"wb")
			for i in range(0, len(result), 2):
				outf.write(binascii.unhexlify(result[i:i+2]))
			outf.close()
			exit()
		else:
			result += data


sniff(offline='exfil.pcapng', filter="icmp", prn=get_payload)
```

Contents of the `out` file:
```console
$ cat out         
[client]
password = PCTF{n0t_4_v3ry_sn34ky_3xf1l}
port = 3306
socket = /run/mysqld/mysqld.sock

[mysqld]
port = 3306
<snip>
```

Looks like a sql db conf file with the flag as the password.