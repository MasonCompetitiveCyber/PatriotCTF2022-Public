# Metro

### Description

We recovered an Android phone from a suspect in the D.C. area. We were able to get a logical image of the device in the form of an ADB backup. We're trying to compile the location history of the suspect, can you figure out which metro station they traveled to on April 7th, 2022?

Flag format: `pctf{Station Name}`, e.g. `pctf{Metro Center}`

### Difficulty

4/10

### Flag

`pctf{Twinbrook}`

### Hints

Try checking the non-default apps.

### Author

Andy Smith

### Tester

### Writeup

Use one of the many existing tools to extract the ADB backup, such as [ABE](https://github.com/nelenkov/android-backup-extractor):

```bash
java -jar abe.jar unpack backup.ab backup.tar
```

Then search through the apps. There is a city transit and navigation app, Citymapper, stored in com.citymapper.app.release.

Inside, there is a db folder with a citymapper.db SQLite database. Opening that in a tool like DB Browser for SQLite will show the tables.

The `savedtripentry` table shows saved and recent trips. The only trip marked `RECENT` is on April 7th, 2022 (from the challenge description). Looking at either the `originalSignature`, `signature`, or `tripData` columns will all show JSON data, with an "end" object specifying that the end station was Twinbrook.

For example, the `signature` columns is:

```json
{
   "car":9377,
   "duration":1070,
   "end":{
      "coords":"39.062696,-77.121216",
      "id":"citymapper:DCStation_Twinbrook",
      "name":"Twinbrook",
      "source":"3"
   },
   "jr_index":0,
   "legs":[
      {
         "distance":71,
         "duration":150,
         "ec":"38.98469,-77.09461",
         "in_station":"0/90",
         "mode":"walk",
         "sc":"38.98472,-77.09463",
         "to_exit":"DCStation_Bethesda_E5075"
      },
      {
         "duration":720,
         "end":"DCStation_Twinbrook",
         "mode":"transit",
         "route_ids":[
            "WMATAMetroRed"
         ],
         "start":"DCStation_Bethesda",
         "stop_count":5,
         "stop_ids":[
            "Platform_DCBethesda_R_SG",
            "Platform_DCTwinbrook_SG"
         ]
      },
      {
         "distance":0,
         "duration":0,
         "ec":"39.06244,-77.12093",
         "mode":"walk",
         "sc":"39.06244,-77.12093"
      }
   ],
   "price_pence":315,
   "region":"us-dc",
   "routing_request_id":"4e1b35b0-4788-41b3-bdb0-27a67eec970a",
   "start":{
      "address":"Wisconsin Avenue",
      "coords":"38.984698,-77.094717",
      "source":"1"
   },
   "time":"2022-04-07T17:43:08-04:00/NOWISH",
   "version":2
}
```
