https://masoncc-patriotctf-2022.s3.amazonaws.com/android-disk002.zip

Android 1:
Our friend accidently deleted a picture of his favorite dog can you figure out what the md5sum of the deleted picture

Android 2:
Find the phone number from the contact in the phone image

Android 3: 
See if you can find email of the owner of the phone

Android 4:
See if you can find the app build number for facebook.

Android 5:
Find the facebook user id for the owner of the phone.


Writeup: 
android 1
  check deleted files and then filesystem then looking at the thumbnail listing
  flag: PCTF{863c2bf4685527570255417b3301aebf}
  
 android 2
  there is a contacts tab in autopsy which is immediately obvious
  flag: PCTF{662-364-5944}
  
  android 3
    email can be found in web accounts tab
    flag: PCTF{bensmith1995masoncc@gmail.com}
    
    
 android 4
  in the installed programs tab you can select library.db in com.facebook.katana and then move out of the com.android.vending folder to com.facebook.katana folder then you can go to /databases where you can get the app versiom from opening composer.db in dbbrowser for SQLite
  flag: PCTF{361571111}
  
  android 5 
      in the installed programs tab you can select library.db in com.facebook.katana and then move out of the com.android.vending folder to com.facebook.katana folder then you can go to /databases where you can get the user id for the facebook profile from composer_db-uid 
      which you can then get the url of the facebook htttps://www.facebook.com/profile.php?id=userid
      flag: PCTF{https://www.facebook.com/profile.php?id=100080118587321}
            PCTF{https://www.facebook.com/profile.php?id=100079925037491}
