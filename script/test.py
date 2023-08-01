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
        'apify_api_key_path': '/TOP/home/kt/API_KEY/apify',
        }
    pet_friendly_judger = PetFriendlyJudger(pfj_src_dict)

    #test place id
    #url = 'https://www.google.com/maps/place/Cotopaxi,+549+Hayes+St,+San+Francisco,+CA+94102,+United+States/@37.7763834,-122.425524,16z/data=!4m6!3m5!1s0x808581f30d9262ef:0xab9d5e26b5c11615!8m2!3d37.7763834!4d-122.425524!16s%2Fg%2F11rdrjyjlk?hl=en-TW&gl=tw'
    url = 'https://www.google.com/maps/place/LuxFit+SF/@37.7763797,-122.4622822,14z/data=!4m7!3m6!1s0x8085818bf590c47d:0xcbbe4b59be76f6d6!8m2!3d37.7763813!4d-122.4241716!15sCgZsdXhmaXRaCCIGbHV4Zml0kgEOZml0bmVzc19jZW50ZXLgAQA!16s%2Fg%2F11mw09lt81?hl=en-TW&entry=tts&shorturl=1'
    reply = pet_friendly_judger.judge_store(url, if_stream=True)
    while True:
        try:
            chunk = next(reply)
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                print(content)
        
        except StopIteration:
            break 
