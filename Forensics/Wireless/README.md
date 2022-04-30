# Wireless

NOTE: if no solves for a while, share `pairing.pcap`. when merged with mouse.pcap it will make it human-readable

### Description
I'm trying to spy on my co-worker because I suspect she spends her work time drawing in MS Paint. I got Wireshark running on her PC, but I can't make sense of these packets. Can you figure out what she is drawing?

p.s. If I'm not mistaken, I think she uses a wireless mouse.

### Difficulty
7/10?

### Flag
`PCTF{i_love_to_draw_with_a_mouse}`

### Hints
1. Figure out the structure for the mouse HID data

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Once you figure out the data structure of the L2CAP packets, it is trivial.

First, if we open `mouse.pcapng`, we will see the following data if we filter by `btl2cap`. The payloads are not very human-readable.
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/l2cap_packets.png" width=60%  height=60%></p>

A decent amount of googling is required to figure out what this data means. If you have a wireless mouse, capturing that data will probably help you figure out what's happening. Make sure you capture the bluetooth pairing of the mouse so wireshark can actually decode these packets, the data will look nice:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/readable-hid.png" width=30%  height=30%></p>

Another good place for packet structure is lines 174-182 of https://github.com/benizi/hidclient/blob/master/hidclient.c:
```c
struct hidrep_mouse_t
{
	unsigned char	btcode;	// Fixed value for "Data Frame": 0xA1
	unsigned char	rep_id; // Will be set to REPORTID_MOUSE for "mouse"
	unsigned char	button;	// bits 0..2 for left,right,middle, others 0
	signed   char	axis_x; // relative movement in pixels, left/right
	signed   char	axis_y; // dito, up/down
	signed   char	axis_z; // Used for the scroll wheel (?)
} __attribute((packed));
```

Let's look at one of the payloads from the pcap: `a10201ff0300`

Comparing with the above code or image, we can decipher that the `a1` byte is the value denoting this is a data packet. `02` is the ID for a mouse. `01` must be some button is pressed (most likely left). `ff` is mouse displacement on the x-axis and `03` is the mouse displacement on the y-axis. The last `00` is for the scroll wheel.

From `a1:02:01:ff:03:00` only really care for bytes index 2,3,4 (button press, x displacement, y displacement). One thing to note, is that the displacement bytes are signed chars (-127 to 127), so `ff` is not 255, but actually `-1`. In this case, we can guess that left mouse button is pressed, x displacement is -1 and y displacement is 3. 

Let's look at one more payload: `a1:02:00:03:fb:00`. This tells us no button is pressed, x displacement is 3, and y displacement is -5 (251 - 256 = -5; or use 2's compelement math)

Here's my script to go through each payload, extract this information, and graph it:
```python
import matplotlib.pyplot as plt
import pyshark

mousePosX = 0
mousePosY = 0

X = []
Y = []

f = pyshark.FileCapture('mouse.pcapng', display_filter="btl2cap")

for p in f:
	data = p['btl2cap'].payload.split(":")
	press = int(data[2],16)
	x_disp = int(data[3],16)
	y_disp = int(data[4],16)

	# disp is a signed char
	if x_disp > 127:
		x_disp -= 256
	if y_disp > 127:
		y_disp -= 256

	mousePosX += x_disp
	mousePosY += y_disp
	
	if press:
		X.append(mousePosX)
		Y.append(-mousePosY)

fig = plt.figure()
ax1 = fig.add_subplot()
ax1.scatter(X, Y)
plt.show()
```

We only want to graph points when the mouse button was pressed but still update the mouse position when it's not pressed. Here is the output graph:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/mouse_graph.png" width=60%  height=60%></p>

It's not the prettiest and doesn't actually line up exactly with my original movements (probably because of bluetooth latency and frequency of sending packetse), but it's readable!
