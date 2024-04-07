# How to run

```sh
cd backend
pip3 install -R requirements.txt
cd src
uvicorn main:app  --host 0.0.0.0 --port 8080 --reload
```

## Setup Mongo

```sh
sudo docker pull mongo:latest
sudo docker run -d -p 27017:27017 --name=mongo mongo:latest
docker exec -it mongo bash
mongosh
use dynamic-survey
db.createCollection("forms")
db.createCollection("survey_bot")
db.forms.drop()
db.survey_bot.drop()
```

### Restart mongo
```sh
sudo docker ps -a
# See the id to start, replace it in the next command
sudo docker start d23830e457a3
# Attach shell to 
sudo docker exec -it d23830e457a3 /bin/bash
```

## Export keys in the environment

```sh
export GOOGLE_OATH_CLIENT_ID="YOUR_GOOGLE_OATH_CLIENT_ID"
export GOOGLE_OATH_CLIENT_SECRET="YOUR_GOOGLE_OATH_CLIENT_SECRET"
```
