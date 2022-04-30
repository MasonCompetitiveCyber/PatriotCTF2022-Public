# Base64 Times 10

### Description
I heard that rot13 and base64 are easily decoded, but I'm sure that it's just because they are only used once. As such, I have masterfully hidden the flag behind 1000 layers of rot13 and 10 layers of base64. It should be pretty much impossible for anyone to get it now!

### Difficulty
1/10

### Flag
`pctf{0bfusc@tion_1s_n0t_3ncrypt10n}`

### Hints
Much like raising a negative number to a power, whether a message is plaintext or scrambled in rot13 depends on if it has been performed an even or odd number of times.

### Author
Maxime Bonnaud (Migyaksuil)

### Tester
None yet

### Writeup

Here is the cihpertext:
```Vm0wd2VHUXhTWGhXV0doVFYwZDRWRll3Wkc5V01WbDNXa1pPVlUxV2NIcFhhMXBQWVd4YWMxWnFUbGROYWtaSVdWZDRZV014VG5OWGJGcE9ZbTFvVVZacVNqUlpWMUpJVm10c2FsSnRVazlaVjNoaFlqRmtXR1JIUmxSTmJFcEpWbGR3WVZaSFNrZGpSVGxhWWxoT00xcFZXbUZqTVhCRlZXeG9hVlpzY0VsV2EyTXhVekpHVjFOdVZsSmlWR3hXVm01d1IyUnNiSEZTYlhSWFRWZFNNRnBGV2xOVWJGcFpVV3h3VjFaNlJYZFdha1poWkVaT2NtSkdTbWxoZWxab1ZtMTBWMWxXV1hoalJscFlZbGhTY1ZsclpGTmxiRmw1VFZSU1ZrMXJXVEpXYlhoelZqSktWVkZZYUZkV1JWcHlWVEJhUzJOV1pITmFSMmhzWWxob2IxWnRNWGRVTWtsNVVtdGthbEpzY0ZsWmJHaFRWMFphZEdONlJsZGlSbG93VkZab2ExWlhTbFpqUldSWFRWWktTRlpxU2t0VFJsWlpXa1prYUdFeGNGaFhiRlpoWkRGS2RGSnJaRmhpVjNodlZGVm9RMkl4V1hoYVJGSnBUVlZXTkZWc2FHOVdiR1JJWVVaU1YyRXlVVEJXVjNoaFZqRldXVnBHUWxaV1JFRTE=```

Doing rot13 1000 times is like never doing it at all so that can be ignored. 10 rounds of base64 encoding can either be decoded manually or with a simple python script.

Here is a quick script to do just that:
```python
flag = [insert cipher text here]

for i in range(10):
    flag_bytes = flag.encode('ascii')
    base64_bytes = base64.b64decode(flag_bytes)
    flag = base64_bytes.decode('ascii')

print(flag)
```
