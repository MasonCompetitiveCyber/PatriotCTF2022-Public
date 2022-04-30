echo 'Its not gonna be that easy!' > /share/flag.txt
chmod 777 /share/flag.txt
setfattr -n 'user.DOSATTRIB' -v '0sAAAEAAQAAABRAAAAIAAAACA9uWhxLNhtZn+4aHEs2AE=' /share/flag.txt
setfattr -n 'user.DosStream.secret:$DATA' -v 'pctf{d0nt_cr055_th3_str34ms!}\015\012' /share/flag.txt
smbd --foreground --no-process-group --configfile /etc/samba/smb.conf