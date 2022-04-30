# Docker
```
unzip TaaS.zip
cd TaaS
sudo docker build -t flask_docker .
sudo docker run -p 5000:5000 -d flask_docker
```
You should now be able to go to http://localhost:5000 and see the web app.

# Manual
```
unzip TaaS.zip
cd TaaS
pip3 install -r requirements.txt
python3 main.py
```

# Admin Creds
`admin:BustyAndTheBass123!$`