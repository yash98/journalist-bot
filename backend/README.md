# How to run

```sh
cd backend
pip3 install -R requirements.txt
cd src
uvicorn main:app  --host 0.0.0.0 --port 8080 --reload
```