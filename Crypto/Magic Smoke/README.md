# Magic Smoke

### Description

Martha manages the production database for her company. She stores encrypted backups in case the database is ever corrupted. Unfortunately, there was a power surge at the office and the server's hard drive let out the magic smoke. When trying to recover from her encrypted backup, Martha realizes she forgot the password. Can you recover the database from her backup?

Flag format: PCTF{}

### Difficulty

5-6/10? Not sure cause it's not actually hard crypto, you just have to take some time to crack it.

### Flag

`PCTF{sh0uld_pr0b4bly_h4ve_a_surg3_pr0t3ctor}`

### Hints

Martha doesn't care about compression, only encryption, so she used ZipCrypto Store instead of Deflate in her ZIP backup. That shouldn't compromise her security right?

### Author

Andy Smith

### Tester

None yet

### Writeup

The file in the zip isn't compressed (i.e. Store) and is encrypted with ZipCrypto. The combination of these two things means it is easy to crack the password given that you know a few bytes of plaintext.

The file inside is a Sqlite3 database, which has a nice long file header of "SQLite format 3", perfect for acting as a known plaintext.

Save that header to a file, making sure there's no trailing whitespace (use a hex editor).

```bash
# xxd hex dump of header.bin
00000000: 5351 4c69 7465 2066 6f72 6d61 7420 3300  SQLite format 3.
```

Download bkcrack, run the following to crack the key:

```bash
# Crack the key
bkcrack.exe -C 'db_backup.zip' -c 'prod_db_backup.sqlite3' -p header.bin
# Paste the 3-part key into the next command to extract the file
bkcrack.exe -C 'db_backup.zip' -c 'prod_db_backup.sqlite3' -k 43b19ad0 43ef0139 ebafb2c5 -d extracted_db.sqlite3
```

The flag is stored in base64 in the only table in the database.

I generated a few ZIPs until the cracking time was small, so if they use bkcrack it should only take up to ~14.4% before its cracked if they use the full length sqlite header as their plaintext.

Example output:

```bash
PS C:\Users\Andy\Downloads\bkcrack-1.3.4-win64> .\bkcrack.exe -C 'db_backup.zip' -c 'prod_db_backup.sqlite3' -p header.bin
bkcrack 1.3.4 - 2022-01-01
[17:19:20] Z reduction using 8 bytes of known plaintext
100.0 % (8 / 8)
[17:19:20] Attack on 813121 Z values at index 7
Keys: 43b19ad0 43ef0139 ebafb2c5
14.4 % (117247 / 813121)
[17:20:45] Keys
43b19ad0 43ef0139 ebafb2c5
PS C:\Users\Andy\Downloads\bkcrack-1.3.4-win64> .\bkcrack.exe -C 'db_backup.zip' -c 'prod_db_backup.sqlite3' -k 43b19ad0 43ef0139 ebafb2c5 -d extracted_db.sqlite3
bkcrack 1.3.4 - 2022-01-01
[17:21:33] Writing deciphered data extracted_db.sqlite3 (maybe compressed)
Wrote deciphered data.
```

### References

-   https://github.com/kimci86/bkcrack
-   https://anter.dev/posts/plaintext-attack-zipcrypto/
