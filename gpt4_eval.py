# import openai
from openai import OpenAI
import json
import argparse
import tqdm
import time

if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--prompt_fp', type=str, default='prompts\summeval\con_detailed.txt')
    argparser.add_argument('--save_fp', type=str, default='results\gpt4_con_detailed_openai.json')
    argparser.add_argument('--summeval_fp', type=str, default='data\summeval.json')
    argparser.add_argument('--key', type=str, required=True)
    argparser.add_argument('--model', type=str, default='gpt-4-0613')
    args = argparser.parse_args()

    # openai.api_key = args.key
    client = OpenAI(api_key=args.key)

    # summeval = json.load(open(args.summeval_fp))
    with open(args.summeval_fp, 'r', encoding='utf-8') as f:
        summeval = json.load(f)[:10]

    prompt = open(args.prompt_fp).read()

    ct, ignore = 0, 0

    new_json = []
    for instance in tqdm.tqdm(summeval):
        source = instance['source']
        system_output = instance['system_output']
        cur_prompt = prompt.replace('{{Document}}', source).replace('{{Summary}}', system_output)
        instance['prompt'] = cur_prompt
        while True:
            try:
                # _response = openai.ChatCompletion.create(
                _response = client.chat.completions.create(
                    model=args.model,
                    messages=[{"role": "system", "content": cur_prompt}],
                    temperature=2,
                    max_tokens=5,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    # logprobs=40,
                    n=20
                )
                time.sleep(0.5)

                # all_responses = [_response['choices'][i]['message']['content'] for i in
                #                  range(len(_response['choices']))]
                all_responses = [choice.message.content for choice in _response.choices]
                instance['all_responses'] = all_responses
                new_json.append(instance)
                ct += 1
                break
            except Exception as e:
                print(e)
                if ("limit" in str(e)):
                    time.sleep(2)
                else:
                    ignore += 1
                    print('ignored', ignore)

                    break

    print('ignored total', ignore)
    with open(args.save_fp, 'w') as f:
        json.dump(new_json, f, indent=4)
