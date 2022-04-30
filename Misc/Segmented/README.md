# Segmented

### Description

I think there's an internal website segmented off from the rest of our target's network. Can you find it? I think it may be in the IP range `172.30.0.0/26`. I also found this SSH keypair, but it doesn't look like I can log in.

Flag format: `PCTF{}`

### Difficulty
Hard

### Flag

`PCTF{th1s_pr0xy_1s_sp0ns0r3d_by_n0rdvpn}`

### Hints

### Author

Andy Smith

### Tester

### Setup

```bash
docker-compose up -d
```

### Writeup

There's an internal web server running on `172.30.0.27` with the flag.

To access it, you need to use the obtained keypair. The public key has a comment of `worker` which is the user.

After SSHing in, you get the message:

```bash
$ ssh worker@chal1.pctf.competitivecyber.club -p 10007 -i id_ed25519
Welcome to WeDigTunnels, Inc.
This is a secure system. NO UNAUTHORIZED ACCESS!
This account is not available
```

This is because there is no login shell. However, you can still forward ports. You can forward individual ports, or setup a SOCKS proxy (preferred) like the following:

```bash
ssh worker@chal1.pctf.competitivecyber.club -p 10007 -i id_ed25519 -D 9050 -N
```

The `-D 9050` starts a SOCKS proxy on that port and `-N` tells SSH to not execute a remote command, which just leaves the connection open.

You don't know which IP address you're trying to access, so you'll need to scan the given IP range. You can just manually try all the IPs, but an easier way is to scan with nmap or loop with curl.

For nmap, you can use proxychains to use the SOCKS proxy.

```bash
proxychains nmap -T4 -Pn -p80 172.30.0.0/26 --open
```

Or you can use a curl command like the following, which will be much quicker than the nmap scan due to the small timeout:

```bash
curl -x socks5h://127.0.0.1:9050 -I 172.30.0.{1..62} --connect-timeout 0.3
```

Either of these should show you which IP has the web server. Then just use curl to get the webpage or set Firefox to use the SOCKS proxy. The flag is in the homepage.
