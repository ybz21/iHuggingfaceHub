<p align="left">
        <a href="README-CN.md">中文</a>&nbsp ｜ &nbspEnglish&nbsp </a>
</p>
<br><br>

# iHuggingfaceHub😜: Your own private huggingface hub server!
# Goal

Make your own huggingface hub with local files.

You can access local model and dataset by using huggingface transformers and datasets lib, just like:
```python
import os
os.environ['HF_ENDPOINT'] = 'http://server-ip:9999'
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True).eval()
```

# Deploy

## Local Mode
```shell
pip3 install -r requirements.txt
python3 app.py
```

## Docker Mode
```shell
docker compose up -d
```

# Usage

step1. put models in 'files' directory

```shell
mkdir -p files/Qwen
cd files/Qwen
git clone https://huggingface.co/Qwen/Qwen-7B-Chat
```

step2. use transformers lib to load model

```python
import os

def main():
    os.environ['HF_ENDPOINT'] = 'http://127.0.0.1:9999'  # change to app.py host ip
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.generation import GenerationConfig
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True).eval()
    generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-7B-Chat", trust_remote_code=True,
                                                         resume_download=True)
    model.generation_config = generation_config
    response, history = model.chat(tokenizer, "你好", history=None)
    print(response)


if __name__ == '__main__':
    main()
```

# TODO
* Add revision support
* Add dataset support