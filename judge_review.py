# +
import os
import openai

from tools import get_file_contents, save_string_to_file, talk2gpt
# -

if __name__ == '__main__':
    TEST_ID = 3
    SAVE_DIR = './sample'
    
    openai.api_key = get_file_contents('./api_key/openai')
    
    guide = get_file_contents(f'{SAVE_DIR}/guide.txt')
    reviews = get_file_contents(f'{SAVE_DIR}/text{TEST_ID}.txt')
    
    save_path = f'{SAVE_DIR}/judge{TEST_ID}.txt'
    
    txt = guide + ': ' + reviews
    judge_result = talk2gpt(txt)

    print(judge_result)
    save_string_to_file(save_path, judge_result)
