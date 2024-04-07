import jsonlines
import os
import json
import subprocess
import csv
import jsonlines

data_path = './results'

def to_csv(dataset, model, in_context_example, is_reverse=False):
    if is_reverse:
        results_path = f'{data_path}/{dataset}/{model}/regex_gen_{in_context_example}_reverse.jsonl'
        csv_path = f'{data_path}/{dataset}/{model}/example_{in_context_example}_reverse.csv'
    else:
        results_path = f'{data_path}/{dataset}/{model}/regex_gen_{in_context_example}.jsonl'
        csv_path = f'{data_path}/{dataset}/{model}/example_{in_context_example}.csv'
    with open(results_path, 'r') as f:
        data = list(f)
    csv_file = open(csv_path, 'a', newline='', encoding='utf8')
    writer = csv.writer(csv_file)
    # 写入列名
    writer.writerow(['Description', 'Gold regex', 'Inference regex'])

    for idx, item in enumerate(data):    
        json_item = json.loads(item)
        description = json_item['description'].strip()
        truth_regex = json_item['truth regex'].strip()
        gpt3_inference = json_item['gpt3 inference regex'].strip()
        writer.writerow([description, truth_regex, gpt3_inference])
    csv_file.close()

def regex_equiv(gold, predicted):
  if gold == predicted:
    return True
  try:
    out = subprocess.check_output(['java', '-jar', './data/regex_dfa_equals.jar', '{}'.format(gold), '{}'.format(predicted)])
    # print("out")
    # print(out)
    if '\\n1' in str(out):
      return True
    else:
      return False
  except Exception as e:
    return False
  return False

def regen_regex_postprocess(gpt_inference):
    if len(gpt_inference) < 1:
        return ''
    gpt_inference = gpt_inference.replace('/', "")
    gpt_inference = gpt_inference.replace('`', "")
    if gpt_inference[-1] == '$':
        gpt_inference = gpt_inference[:-1]
    if gpt_inference[0] == '^':
        gpt_inference = gpt_inference[1:]
    return gpt_inference

def check_dfa(dataset, prompt_type, model, in_context_example, is_reverse=False):
    if is_reverse:
        results_path = f'{data_path}/{dataset}/{model}/{prompt_type}/regex_gen_{in_context_example}_reverse.jsonl'
    else:
        results_path = f'{data_path}/{dataset}/{model}/{prompt_type}/regex_gen_{in_context_example}.jsonl'
    with open(results_path, 'r') as f:
        data = list(f)
    count = 0
    with jsonlines.open('diff.jsonl', "a") as file:
        gen_list = []
        for idx, item in enumerate(data):
            regex_generation = {}    
            json_item = json.loads(item)
            truth_regex = json_item['truth regex'].strip()
            gpt_inference = json_item['gpt inference regex'].strip()
            gpt_inference = regen_regex_postprocess(gpt_inference)
            if len(gpt_inference) > 0 and regex_equiv(truth_regex, gpt_inference):
                count += 1
            # else:
            #     regex_generation["index"] = json_item['index']
            #     regex_generation["description"] = json_item['description']
            #     regex_generation["truth regex"] = json_item['truth regex']
            #     regex_generation["gpt3 inference regex"] = json_item['gpt3 inference regex']

            #     gen_list.append(regex_generation)
        # file.write_all(gen_list)
        
        # print(f'{idx + 1}:')
        # print(json_item['description'])
        # print(f'{truth_regex}  |  {gpt3_inference}')
    return count * 1.0 / len(data)

def check_em(dataset, prompt_type, model, in_context_example, is_reverse=False):
    if is_reverse:
        results_path = f'{data_path}/{dataset}/{model}/{prompt_type}/regex_gen_{in_context_example}_reverse.jsonl'
    else:
        results_path = f'{data_path}/{dataset}/{model}/{prompt_type}/regex_gen_{in_context_example}.jsonl'
    with open(results_path, 'r') as f:
        data = list(f)
    count = 0
    for idx, item in enumerate(data):
        json_item = json.loads(item)
        truth_regex = json_item['truth regex'].strip()
        gpt_inference = json_item['gpt inference regex'].strip()
        gpt_inference = regen_regex_postprocess(gpt_inference)
        # print(truth_regex +" || " + gpt3_inference)
        # print(str(idx) + ": " + truth_regex +" || " + gpt3_inference)
        if truth_regex == gpt_inference:
            # print(truth_regex +" || " + gpt3_inference)
            count += 1
        
        # print(f'{idx + 1}:')
        # print(json_item['description'])
        # print(f'{truth_regex}  |  {gpt3_inference}')
    return count * 1.0 / len(data)

def main():
    dataset = 'KB13' # 'KB13' | 'Truk'
    model = "gpt-3.5-turbo" # "gpt-4" | "gpt-3.5-turbo"
    prompt_type = 'least_to_most_prompting' # analogical_prompting | least_to_most_prompting
    in_context_example = 6
    is_reverse = False
    em = check_em(dataset, prompt_type, model, in_context_example, is_reverse=is_reverse)
    print(f"Example num: {in_context_example}, EM: {em}")
    dfa = check_dfa(dataset, prompt_type, model, in_context_example, is_reverse=is_reverse)
    print(f"Example num: {in_context_example}, DFA: {dfa}")
    # print(regex_equiv("(([a-z])|([A-Z])){5,}", "[a-zA-Z]{5,}"))
    # print(regex_equiv('.*bar.*', 'bar'))
    # to_csv(dataset, model, in_context_example, is_reverse=is_reverse)

if __name__ == "__main__":
    main()