# Docker
```
docker pull nickgryg/alpine-pandas
unzip ExcellentDatabase.zip
cd ExcellentDatabase
sudo docker build -t flask_docker .
sudo docker run -p 5000:5000 -d flask_docker
```
You should now be able to go to http://localhost:5000/ and see the web app.

# Manual
```
unzip ExcellentDatabase.zip
cd ExcellentDatabase
pip3 install -r requirements.txt
apt install libreoffice
python3 main.py
```