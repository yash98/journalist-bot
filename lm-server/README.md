# How to run

```sh
cd lm-server
pip3 install -R requirements.txt
uvicorn run_gemma-7it:app --host 0.0.0.0 --port 8000 --reload
```

## vLLM
### Setup
```sh
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo apt install nvidia-docker2
git clone https://github.com/yash98/vllm.git
cd vllm
sudo docker build -t custom-vllm-image .
```

### Startup
```sh
sudo docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HF_AUTH" \
    -p 8000:8000 \
    --ipc=host \
    custom-vllm-image \
    --model TechxGenus/gemma-7b-it-GPTQ
```

### Restart
```sh
sudo docker ps -a
# See the id to start, replace it in the next command
sudo docker start 15856cb7c3e7
# Attach shell to 
sudo docker exec -it 15856cb7c3e7 /bin/bash
```

### Curls
```
curl http://localhost:8000/v1/models
curl http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "TechxGenus/gemma-7b-it-GPTQ",
"messages": [
{"role": "user", "content": "You are a helpful assistant. Who won the world series in 2020?"}
]
}'
```