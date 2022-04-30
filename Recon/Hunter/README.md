# Hunter

### Description
I took this photo on 4/29/22 around Noon after I landed. Which city did I just arrive from?

Flag format: PCTF{city}

### Difficulty
Hard

### Flag
`PCTF{Chicago}`

### Hints

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Here is the image:
<img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/Recon/Hunter/hunter.png" width=40%  height=40%>

The tail has an image of a puffin. This is Frontier's plane: https://www.flyfrontier.com/plane-tails/sky-animals/captain-the-puffin/?mobile=true

The aircraft is `N322FR`, this alone will give you a lot of info. Go here: https://flightaware.com/live/flight/N322FR and you'll see past flights. One arrived at DCA gate 7 around 12:45 on 4/29/22. This is where the photo must have been taken. The image is of a plane to the right of the current gate. Frontier will always go to Terminal A at DCA. We need to find a plane that arrived right before at DCA terminal A gate 8 (the one to the right). This link: https://www.flightstats.com/v2/flight-tracker/arrivals/DCA/WN?year=2022&month=4&date=29&hour=12 with the right parameters will show you several options. Here's the flight: https://www.flightstats.com/v2/flight-tracker/WN/510?year=2022&month=4&date=29&flightId=1090431829

We filter by southwest because Terminal A only services Southwest, Frontier, and AirCanada.


