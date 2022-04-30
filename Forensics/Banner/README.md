# Banner

### Description
I was told to find the secret message being sent over this packet capture, but I'm stumped. Can you figure it out? I was told it has something to do with a banner?

### Difficulty
Medium

### Flag
`PCTF{just_at3_ch1ck3n_nugg3ts}`

### Hints
file carving

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

This challenge involves binwalking a squashfs filesystem from TCP data in a pcap. We see this packet in the pcap:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/pcap_messages.png" width=40%  height=40%></p>

Follow the TCP stream and some data being sent:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/banner_data.png" width=60%  height=60%></p>

Conver it to "Raw" and wait for all of it to load before saving. Once that's done, let's run binwalk on it:

```console
$ binwalk data         

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
9176178       0x8C0472        Squashfs filesystem, little endian, version 4.0, compression:gzip, size: 17573585 bytes, 2603 inodes, blocksize: 131072 bytes, created: 2022-03-24 21:46:19
```

Let's extract it with `binwalk -e data`:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/banner_extracted.png" width=60%  height=60%></p>

If you just do some quick enumeration, you'll see an `etc/banner` file (this exists because this the filesystem of TP-Link Router Firmware, which store their banner in `etc/banner`).

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/banner_flag.png" width=60%  height=60%></p>
