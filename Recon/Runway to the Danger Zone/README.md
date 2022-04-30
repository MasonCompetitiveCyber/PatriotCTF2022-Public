# Runway to the Danger Zone

### Description
Our satellite images have picked up this image of three unidentified aircraft at an airbase, however, we have no idea which one. You're one of our top analysts and we know you are gunning for a promotion so we've given the task to you. Find us the IATA code of the airport in question and enclose it in PCTF{} to complete this task.

Example flag:
PCTF{airportcode}

### Difficulty
Hard

### Flag
`PCTF{IFN}`

### Hints
Hint 1: This aircraft leaves quite a memorable impression. So much so that it was the main aircraft in a film featuring Tom Cruise back in 1986.

Hint 2: Despite its strengths, this aircraft is showing its age and only one country still fields it to this day.

Hint 3: The airport you are looking for ends in 'an'

### Author
Maxime Bonnaud (Migyaksuil)

### Tester
None yet

### Writeup

Here is the image provided:
<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/cool_planes.png" width=40%  height=40%></p>

Visible in this image is a clearly sandy environment, some hangars, and the stars of the show: three Iranian F-14 Tomcats. If you aren't an aviation geek like me, the challenge title "Runway to the Danger Zone" alludes to the song 'Highway to the Danger Zone' which featured in the film Top Gun that has the iconic Tomcat as its main aircraft. The film's title is also hinted at in the phrase "You're one of our **top** analysts and we know you are **gunning** for a promotion so we've given the task to you". The aircraft has an incredibly distinct and unique silhouette, so even if these hints aren't picked up on, a google search of "fighter jets" will give the F-14 as one of its results which can then be used to pinpoint the aircraft.

Following up on this hint, we can see that this aircraft has only been fielded by two countries: The United States and Iran. The United States have since retired the aircraft and since we assume the image has been taken somewhat recently, that only leaves Iran. 

Searching around for Iranian Air bases nets a wikipedia page simply titled "List of Iranian Air Force bases" and a list that contains the following:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF2022-Public/raw/main/writeup-images/Iranian_Tactical_Airbases.png" width=60%  height=60%></p>

We can see that only two airbases are rumored to have F-14s: Isfahan and Mehrabad.

From there some digging around both airports (Isfahan has a large array of silos detached from the main runway, while Mehrabad does not) will reveal the silos in question and a quick google search will yield the IATA airport code of Isfahan as "IFN". 

