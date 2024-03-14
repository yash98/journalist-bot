# How to run

```sh
cd lm-server
pip3 install -R requirements.txt
uvicorn run_gemma-7it:app --host 0.0.0.0 --port 8000 --reload
```

## vLLM
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
sudo docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HF_AUTH" \
    -p 8000:8000 \
    --ipc=host \
    custom-vllm-image \
    --model TechxGenus/gemma-7b-it-AWQ
```