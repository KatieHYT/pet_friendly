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
    answer, reason = pet_friendly_judger.judge_store(place_id)
    reason = remove_empty_lines(reason)
    storeid2storename_map = read_json(pfj_src_dict['storeid2storename_map_path'])
    print(place_id)
    store_name = storeid2storename_map[place_id]
    print(f'Is {store_name} pet-friendly? \n{answer}\n\t{reason}')
