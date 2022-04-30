# Waffle Cabin

### Description
I ate this really amazing waffle after some icy runs, but through an unkown series of events that I don't have the creativity to come up with, I completely forgot where this was. Can you help me locate the ski resort this was at?

Flag format: `PCTF{Full_Resort_Name}`

### Difficulty
Medium

### Flag
`PCTF{Okemo_Mountain_Resort}`

### Hints
Resorts tend to have slightly different Ski instructor jackets/uniforms.

### Author
Daniel Getter (NihilistPenguin)

### Tester
None yet

### Writeup

Here is the image:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/Recon/Waffle%20Cabin/challenge.png" width=40%  height=40%></p>

The first step is obviously to google "Waffle Cabin" or go to their website written on the sign (https://wafflecabin.com/). There are around 35 locations listed, and most have photos. Most of the ones with photos have do not look exactly like the one we have. There are only some that look similar, such as Okemo, Belleayre, Pico,Bretton Woods, Loon Mountain, and Mount Sunapee. Some of these have buildings in the background that would rule them out as candidates. The two trees behind the waffle cabin may be enough for some people to be confident with Okemo. One unique thing about this image is the skiier in the background on the right is wearing a full blue ski outfit.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/PatriotCTF-2022/raw/main/writeup-images/ski_instructor_from_pic.png" width=40%  height=40%></p>

This guy is actually a ski instructor, and ski instructors at different resorts have generally different "uniforms". This one looks like it could be Okemo or Mount Sunapee. 

<p align="center">
    <img src="https://dam-assets.vailresorts.com/is/image/vailresorts/20201220_OK_Employee_004_1002x668?wid=360&fit=constrain,1&fmt=png-alpha&resMode=sharp2&dpr=on,1" width=40%  height=40%><br>
    <em>Okemo Ski Instructor from https://www.okemo.com/plan-your-trip/ski-and-ride-lessons.aspx</em>
</p>

<p align="center">
    <img src="https://dam-assets.vailresorts.com/is/image/vailresorts/20200224_MS_Davies_026_1002x668?wid=585&fit=constrain,1&fmt=png-alpha&resMode=sharp2&dpr=on,1" width=60%  height=60%><br>
    <em>Mount Sunapee Ski Instructor from https://www.mountsunapee.com/plan-your-trip/ski-and-ride-lessons/category/private?lessonTypes=Private&sports=Ski</em>
</p>

Googling more about both of these resorts and their waffle cabins, you should be confident enough to say it's `Okemo Mountain Resort`.  
