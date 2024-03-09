# How to run

```sh
cd lm-server
pip3 install -R requirements.txt
uvicorn run_gemma-7it:app --host 0.0.0.0 --port 8000 --reload
```