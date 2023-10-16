import os


def main():
    os.environ['HF_ENDPOINT'] = 'http://127.0.0.1:9999'  # change to app.py host ip

    # must import transformers after set HF_ENDPOINT env
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
