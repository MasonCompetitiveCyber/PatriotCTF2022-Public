# Snap

### Description
We have been trying to track down a criminal on the run for several weeks. Yesterday we found and added her on Snapchat using a fake account and she added us back. Luckily for us, she has her Snap Map on. We have taken screenshots of the last 3 times her Snap Map updated with her current location. We need you to figure out the next place she will be so we can intercept her. 

Flag format: `PCTF{Full_Google_Maps_Location_Name}`

### Difficulty
2/10? Not sure yet.

### Flag
`PCTF{Weigh_Station:_Trinidad}`

I will also make `PCTF{Weigh_Station_Trinidad}` a valid flag.

### Hints
There is something in common between all locations.

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup
Here are the three screenshots:

<p align="left">
<img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/Recon/Snap/first.png" width=33%  height=33%>
<img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/Recon/Snap/second.png" width=33%  height=33%>
<img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/Recon/Snap/third.png" width=33%  height=33%>
</p>

If you find those places on google maps and look around for a bit, you should notice that each one has some sort of weigh station or truck scale. We can also see that the person is traveling south on I-25. Searching south of the last stop in Pueblo for truck weigh stations, the next one is `Weigh Station: Trinidad`.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/trinidad_map.png" width=40%  height=40%></p>

