import ast
import os
import random
from typing import Dict, List

import openai

from inference.api_request import create_chatgpt_config, request_chatgpt_engine


class ChatGPTGen:
    def __init__(self, system_message, prompt, model='gpt-3.5-turbo'):
        super().__init__()
        self.system_message = system_message
        self.prompt = prompt
        self.iteration = 20
        self.model = model
        openai.api_base = ""
        openai.api_key = ""

    # @staticmethod
    # def _parse_ret(ret: Dict) -> List:
    #     rets = []
    #     output = ret["choices"][0]["message"]["content"]
    #     if "```" in output:
    #         for x in output.split("```")[1].splitlines():
    #             if x.strip() == "":
    #                 continue
    #             # try:
    #             #     # remove comments
    #             #     input = ast.literal_eval(f"[{x.split('#')[0].strip()}]")
    #             # except:  # something wrong.
    #             #     continue
    #             rets.append(input)
    #     return rets

    @staticmethod
    def _parse_ret(ret: Dict) -> List:
        rets = []
        # print(len(ret["choices"]))
        # print(ret["choices"])
        output = ret["choices"][0]["message"]["content"]
        # print("------")
        # print(output)
        # print("------")
        return output
        # for x in output.splitlines():
        #     if x.strip() == "":
        #         continue
        #     # try:
        #     #     # remove comments
        #     #     input = ast.literal_eval(f"[{x.split('#')[0].strip()}]")
        #     # except:  # something wrong.
        #     #     continue
        #     rets.append(x)
        # return rets, '\n'.join(rets)

    def generate(self):
        config = create_chatgpt_config(self.prompt, max_tokens=2048, system_message=self.system_message, model=self.model)
        ret = request_chatgpt_engine(config)
        return self._parse_ret(ret)
