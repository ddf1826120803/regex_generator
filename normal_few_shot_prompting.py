"""
Regex generation examples
"""

import argparse
import json
import jsonlines
import os
import sys
sys.path.append("../regex_gen")
from inference.gpt_generator import ChatGPTGen

def read_data_sources(data_path):
    with open(os.path.join(data_path, 'SBert.jsonl'), 'r') as f:
        data = list(f)
    count = 0
    dataset = []
    for item in data:    
        json_item = json.loads(item)
        count += 1
        dataset.append(json_item)
    print(f'Loaded {count} regex items')
    return dataset


# class SetEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, set):
#             return list(obj)
#         return json.JSONEncoder.default(self, obj)

def construct_examples(examples, num, reverse=False):
    if num < 1:
        return ''
    prompt = ''
    for i in range(num):
        if reverse:
            ex = examples[num - i - 1]
        else:
            ex = examples[i]
        prompt += "Desciption: " + ex['src']
        prompt += "Regex: " + ex['targ']
    return prompt


def regex_generation(args, regex_data):
    gen_list = []
    with jsonlines.open(args.output, "a") as file:
        for idx, item in enumerate(regex_data):
            regex_generation = {}

            index = item['index']
            description = item['src']
            truth_regex = item['targ']

            prompt = construct_examples(item['top_5'], args.example_num, args.reverse)
            prompt += "Desciption: " + description
            prompt += "Regex: "

            # print("--------Prompt: -------------")
            # print(prompt)
            # break
            # print("1. Start generating regex.......")
            response = ChatGPTGen(prompt=prompt, model=args.model).generate()
            print("-----------Regex generation: ------------")
            print(f"{idx}: Regex desciption:     {description.strip()}")
            print(f"Truth regex:          {truth_regex.strip()}")
            print(f"GPT3 inference regex: {response}")
            # break

            regex_generation["index"] = index
            regex_generation["description"] = description
            regex_generation["truth regex"] = truth_regex
            regex_generation["gpt3 inference regex"] = response

            gen_list.append(regex_generation)
        file.write_all(gen_list)


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--dataset", required=True, type=str)
    # parser.add_argument("--chatgpt_len", required=True, type=int)
    # parser.add_argument(
    #     "--output", default=None, type=int, help="Output .jsonl file name."
    # )
    args = parser.parse_args()
    dataset = 'KB13'
    data_path = f'./data/{dataset}'
    args.example_num = 5
    args.reverse = True
    args.model = "gpt-4" # "gpt-4" | "gpt-3.5-turbo"
    if args.reverse:
        args.output = f'./results/{dataset}/{args.model}/regex_gen_{args.example_num}_reverse.jsonl'
    else:
        args.output = f'./results/{dataset}/{args.model}/regex_gen_{args.example_num}.jsonl'

    regex_data = read_data_sources(data_path)

    regex_generation(args, regex_data)

if __name__ == "__main__":
    main()