"""
Regex generation examples: Analogical Prompting
"""
import argparse
import json
import os
import sys
import re
from tqdm import tqdm
import jsonlines
sys.path.append("../regex_gen")
from inference.gpt_generator import ChatGPTGen
import constants

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

def regex_generation_single(system_message, prompt_message, model):
    response = ChatGPTGen(system_message=system_message, prompt=prompt_message).generate()
    print("-----------Regex generation: ------------")
    print(f"Regex generation problem:\n{prompt_message}")
    print(f"-------------------GPT3 Output:------------------\n{response}")
            

def regex_generation(args, regex_data):
    idx = 0
    gen_list = []
    with jsonlines.open(args.output, "a") as file:
        for item in tqdm(regex_data):
            idx += 1
            if idx == 2:
                break
            regex_generation = {}
            index = item['index']
            truth_regex = item['targ'].strip()

            description = item['src'].strip()
            if description[-1] == '.':
                description = description[:-1]
            
            system_message = constants.ANALOGICAL_PROMPT_SYSTEM_MESSAGE
            prompt = constants.ANALOGICAL_PROMPT_Part1 + description + constants.ANALOGICAL_PROMPT_Part2

            print("--------Prompt: -------------")
            print(prompt)
            print("1. Start generating regex.......")
            response = ChatGPTGen(system_message=system_message, prompt=prompt).generate()
            print("-----------Regex generation: ------------")
            print(f"Regex desciption:     {item['src'].strip()}")
            print(f"Truth regex:          {truth_regex}")
            print(response)

            # findall = re.findall(r'\\boxed{.*}', response)
            # if len(findall) > 0:
            #     inference_answer = findall[-1][7:-1]
            # else:
            #     inference_answer = ''
            # print(f"Model {args.model} inference regex: {inference_answer}")
        #     regex_generation["index"] = index
        #     regex_generation["description"] = item['src']
        #     regex_generation["truth regex"] = truth_regex
        #     regex_generation["gpt inference regex"] = inference_answer

        #     gen_list.append(regex_generation)
        # file.write_all(gen_list)

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
    args.model = "gpt-4" # "gpt-4" | "gpt-3.5-turbo"
    args.output = f'./results/{dataset}/{args.model}/analogical_prompting/regex_gen.jsonl'

    regex_data = read_data_sources(data_path)

    regex_generation(args, regex_data)

    # system_message = constants.ANALOGICAL_PROMPT_SYSTEM_MESSAGE
    # prompt_message = constants.ANALOGICAL_PROMPT

    # system_message = constants.NORMAL_PROMPT_FEW_SHOT_SYSTEM_MESSAGE
    # prompt_message = constants.NORMAL_PROMPT_FEW_SHOT
    # description = "lines that include three capital letters, use '*' to match the whole line.\n"
    # regex_generation_single(system_message, prompt_message, args.model)

if __name__ == "__main__":
    main()