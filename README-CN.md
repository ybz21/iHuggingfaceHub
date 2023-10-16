# iHuggingfaceHub😜: 你自己的私有Huggingface仓库！
# 目标

使用本地文件创建自己的 Huggingface Hub(私有仓库)服务器。

您可以使用 Hugging Face Transformers 和 Datasets 库访问本地模型和数据集，就像这样：

```python
import os
from transformers import AutoModelForCausalLM
os.environ['HF_ENDPOINT'] = 'http://server-ip:9999'  
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True).eval()
```

# 部署

## 本地模式
```shell
pip3 install -r requirements.txt
python3 app.py
```

## Docker模式
```shell
docker compose up -d
```

# 使用

step1. 将模型文件放到files目录

```shell
mkdir -p files/Qwen
cd files/Qwen
git clone https://huggingface.co/Qwen/Qwen-7B-Chat
```

step2. 加载私有仓库的模型

```python
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig


def main():
    os.environ['HF_ENDPOINT'] = 'http://127.0.0.1:9999'  # change to app.py host ip
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
* 增加版本（revision）支持
* 增加数据集（dataset） 支持