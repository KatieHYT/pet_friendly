import os
import json
from pprint import pprint
import openai

from pet_friendly.pet_friendly_judger import PetFriendlyJudger
from pet_friendly.tools import (
        get_file_contents,
        save_string_to_file,
        read_json,
        talk2gpt,
        remove_empty_lines,
        )

if __name__ == '__main__':
    raw_review_dir = '/TOP/home/kt/DATA/cradle/google_review/raw_review/'
    place_id_list = os.listdir(raw_review_dir)
    storeid2storename_map = read_json('/TOP/home/kt/DATA/cradle/google_review/storeid2storename_map.json')

    openai.api_key = get_file_contents('/TOP/home/kt/API_KEY/openai')
    pet_friendly_judger = PetFriendlyJudger()

    #test place id
    place_id = place_id_list[3]
    answer, reason = pet_friendly_judger.judge_store(place_id)
    reason = remove_empty_lines(reason)
    store_name = storeid2storename_map[place_id]
    print(f'Is {store_name} pet-friendly? \n{answer}\n\t{reason}')
