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
