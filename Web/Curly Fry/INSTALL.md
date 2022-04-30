# Docker
```
unzip CurlyFry.zip
cd CurlyFry
sudo docker build -t go_docker .
sudo docker run -p 80:80 -d go_docker
```
You should now be able to go to http://localhost/ and see the web app.

# Manual
```
do all the prerequisite stuff you have to do to run golang, idk, google this
unzip CurlyFry.zip
cd CurlyFry
mv recipe.txt /root/recipe.txt
go run main.go
```