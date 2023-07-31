import os
import sys
import json
from pprint import pprint
import openai

sys.path.append("..")
from src.pet_friendly_judger import PetFriendlyJudger
from src.tools import (
        get_file_contents,
        save_string_to_file,
        read_json,
        talk2gpt,
        remove_empty_lines,
        )

if __name__ == '__main__':
    raw_review_dir = '/TOP/home/kt/DATA/cradle/google_review/raw_review/'
    place_id_list = os.listdir(raw_review_dir)
    openai.api_key = get_file_contents('/TOP/home/kt/API_KEY/openai')
    pfj_src_dict = {
        'raw_review_dir': '/TOP/home/kt/DATA/cradle/google_review/raw_review/',
        'filter_review_dir': '/TOP/home/kt/DATA/cradle/google_review/filtered_review/',
        'guide_path': '/TOP/home/kt/DATA/cradle/google_review/sample/guide.txt',
        'storeid2storename_map_path': '/TOP/home/kt/DATA/cradle/google_review/storeid2storename_map.json',
        }
    pet_friendly_judger = PetFriendlyJudger(pfj_src_dict)

    #test place id
    place_id = place_id_list[3]
    reply= pet_friendly_judger.judge_store(place_id, if_stream=True)
    storeid2storename_map = read_json(pfj_src_dict['storeid2storename_map_path'])
    store_name = storeid2storename_map[place_id]
    print(f'Store Name: {store_name}')
    while True:
        try:
            chunk = next(reply)
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                print(content)
        
        except StopIteration:
            break 
