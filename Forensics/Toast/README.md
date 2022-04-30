# Toast

### Description
We received a report from a user about *sus*picious notifications on their machine. We managed to grab a dump of their Windows notification database, but we can't seem to find any entries that match what the user described. Maybe you can find what we couldn't?

The flag is the handler id of the notification. For example, if the handler was 357, the flag would be PCTF{357}

### Difficulty
Easy

### Flag
`PCTF{114}`

### Hints
SQLite Databases can sometimes have items removed but still present in the file.

### Author
Matthew Johnson (Meat Ball)

### Writeup
To solve this challenge, first understand that you're looking for a removed listing in the notification table of the database. Use your favorite tool for sqlite recovery (I'm using [fqlite](https://www.staff.hs-mittweida.de/~pawlaszc/fqlite/) to browse the removed item)

From there, the challenge title of "Toast" hints that this is a toast notification. Using this, we can sort the removed items by notification type, yeilding only two notifications.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/fqlite.png"></p>

Decoded, the notification payload is:
```
<toast>
	<visual>
		<binding template="ToastText02">
			<text id="1">PatriotCTF Service</text>
			<text id="2">You finally found me! The solution is the handler id for this notification!</text>
		</binding>
	</visual>
</toast>
```

As the instructions indicated, the flag is the handler id for this notification, `PTCF{114}`.

