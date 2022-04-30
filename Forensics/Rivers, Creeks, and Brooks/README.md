# Rivers, Creeks, and Brooks

### Description

Can you find the flag on our file server?

Flag format: `pctf{}`

### Difficulty

4/10?

### Flag

`pctf{d0nt_cr055_th3_str34ms!}`

### Hints

### Author

Andy Smith

### Tester

### Setup

Needs port 445

```bash
cd rivers_creeks_brooks
sudo docker-compose build
sudo docker-compose up -d
```

### Writeup

The share contains a flag.txt file. The flag is stored in an NTFS Alternate Data Stream called `secret`. To get it, the easiest way is to just use Windows.

Just go to `\\chal.competitivecyber.club\` in Windows Explorer and copy the flag.txt file to your local computer.

Then use PowerShell to list the streams and get the content:

```powershell
PS C:\> Get-Item .\flag.txt -Stream *


PSPath        : Microsoft.PowerShell.Core\FileSystem::C:\flag.txt::$DATA
PSParentPath  : Microsoft.PowerShell.Core\FileSystem::C:\
PSChildName   : flag.txt::$DATA
PSDrive       : C
PSProvider    : Microsoft.PowerShell.Core\FileSystem
PSIsContainer : False
FileName      : C:\flag.txt
Stream        : :$DATA
Length        : 28

PSPath        : Microsoft.PowerShell.Core\FileSystem::C:\flag.txt:secret
PSParentPath  : Microsoft.PowerShell.Core\FileSystem::C:\Downloads
PSChildName   : flag.txt:secret
PSDrive       : C
PSProvider    : Microsoft.PowerShell.Core\FileSystem
PSIsContainer : False
FileName      : C:\flag.txt
Stream        : secret      <------ **this is the alternate stream**
Length        : 31



PS C:\> Get-Content .\flag.txt -Stream secret
pctf{d0nt_cr055_th3_str34ms!}
```

Or use command prompt:

```cmd
more < flag.txt:secret
```
