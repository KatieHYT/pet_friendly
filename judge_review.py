import os
import openai

from tools import get_file_contents, save_string_to_file

if __name__ == '__main__':
    TEST_ID = 3
    SAVE_DIR = './sample'
    
    openai.api_key = get_file_contents('./api_key/openai')
    guide = get_file_contents(f'{SAVE_DIR}/guide.txt')
    reviews = get_file_contents(f'{SAVE_DIR}/text{TEST_ID}.txt')
    
    
    save_path = f'{SAVE_DIR}/judge{TEST_ID}.txt'
    
    txt = guide + ': ' + reviews

    msg = {
        "role": "user",
        "content": txt,
    #     "temperature": 0.5,
    #     "top_p": 0.1,
        "name": "kt",
    }

    # create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            msg
        ],
    #     temperature=1,
    #     top_p=0.1,
    #     n=3,
    )

    judge_result = chat_completion.choices[0].message.content
    print(judge_result)
    save_string_to_file(save_path, judge_result)
