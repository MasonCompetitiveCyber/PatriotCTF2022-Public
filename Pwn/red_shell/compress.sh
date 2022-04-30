#!/bin/sh


cp ../redshll ./initramfs/root
cp ../flag ./initramfs
cd initramfs
find . -print0 \
| cpio --null -ov --format=newc \
| gzip -9 > ../initramfs.cpio.gz
#mv ./initramfs.cpio.gz ../
