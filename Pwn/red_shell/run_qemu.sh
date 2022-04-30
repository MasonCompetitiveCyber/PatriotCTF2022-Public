timeout --foreground 180 qemu-system-x86_64 -kernel vmlinuz -initrd initramfs.cpio.gz  -m 128M -monitor /dev/null -nographic -no-reboot -append "console=ttyS0"
