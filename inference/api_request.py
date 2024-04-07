import time
from typing import Dict

import openai

def create_chatgpt_config(
    message: str,
    max_tokens: int,
    temperature: float = 0,
    batch_size: int = 1,
    system_message: str = "You are a helpful assistant doing generation of regular expression.",
    model: str = "gpt-3.5-turbo",
    # model: str = "gpt-4",
) -> Dict:
    config = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "n": batch_size,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": message},
        ],
    }
    return config

def request_chatgpt_engine(config) -> Dict:
    print("Start chagpt request engine")
    ret = None
    while ret is None:
        try:
            ret = openai.ChatCompletion.create(**config)
        except openai.error.InvalidRequestError as e:
            print(e)
        except openai.error.RateLimitError as e:
            print("Rate limit exceeded. Waiting...")
            time.sleep(5)
        except openai.error.APIConnectionError as e:
            print("API connection error. Waiting...")
            time.sleep(5)
        except Exception as e:
            print("Unknown error. Waiting...")
            print(e)
            time.sleep(1)
    return ret
