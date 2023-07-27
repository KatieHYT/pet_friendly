import os
import json
from pprint import pprint
import openai

from .tools import (
        get_file_contents,
        save_string_to_file,
        read_json,
        talk2gpt,
        remove_empty_lines,
        )

class PetFriendlyJudger():
    def __init__(self):
        #TODO(hyt): an assertion to check if openai's api key has been activated
        #TODO(hyt): find a way to load paths
        self.raw_review_dir = '/TOP/home/kt/DATA/cradle/google_review/raw_review/'
        self.filter_review_dir = '/TOP/home/kt/DATA/cradle/google_review/filtered_review/'
        self.guide_path = '/TOP/home/kt/DATA/cradle/google_review/sample/guide.txt'
        self.storeid2storename_map = read_json('/TOP/home/kt/DATA/cradle/google_review/storeid2storename_map.json')

    def _check_store_attr(self, place_id):
        place_dir = os.path.join(self.raw_review_dir, place_id)
        review_id_list = os.listdir(place_dir)
        fn = review_id_list[0]
        file_path = os.path.join(place_dir, fn)
    
        # apify save store info into every review, so we only parse the first one
        _review1 = read_json(file_path)
        _addit_info = _review1['additionalInfo']
        for k, v in _addit_info.items():
            if k == 'Pets':
                #TODO(yth): finish it once you parse a store with this attribute, skip it for now
                assert 1==0

        return None

    def _gather_judge_input(self, guide_path, fn_path_list):
        guide = get_file_contents(guide_path)
        review_list = [get_file_contents(_fn) for _fn in fn_path_list]
        reviews = "\n".join(review_list)
        txt = guide + ': ' + reviews
    
        return txt
    
    def _gen_placeid2storename(self, save_path='./storeid2storename_map.json'):
        place_id_list = os.listdir(self.raw_review_dir)
        place_id_w_keyword_list = os.listdir(self.filter_review_dir)
        
        storeid2storename_map = {}
        for _idx, place_id in enumerate(place_id_list):
            place_dir = os.path.join(self.raw_review_dir, place_id)
            review_id_list = os.listdir(place_dir)
            fn = review_id_list[0]
            file_path = os.path.join(place_dir, fn)
        
            # apify save store info into every review, so we only parse the first one
            _review1 = read_json(file_path)
            
            place_name = _review1['title']
            storeid2storename_map[place_id] = place_name
        
            with open(save_path, 'w') as f:
                json.dump(storeid2storename_map, f)
            print(f'Saved to: {save_path}')

    def judge_store(self, place_id):
        place_id_w_keyword_list = os.listdir(self.filter_review_dir)
        
        # check the attribute that stores set by themselves on google map
        result = self._check_store_attr(place_id)
        if result is not None:
            answer = result
            reason = 'It is shown in google map.'
        else:
            # no review talk about it, return neutral
            if not (place_id in place_id_w_keyword_list):
                answer = 'Neutral'
                reason = 'Not shown in google map and there is no review about it.'
            else: # ask ChatGPT to judge the review
                place_id_w_keyword_dir = os.path.join(self.filter_review_dir, place_id)
                fn_list = os.listdir(place_id_w_keyword_dir)
                fn_path_list = [os.path.join(place_id_w_keyword_dir, _fn) for _fn in fn_list]
                judge_input = self._gather_judge_input(self.guide_path, fn_path_list)
                judge_result = talk2gpt(judge_input)
                
                # we ask chatgpt use @@@@@ to seperate answer and reason.
                answer, reason = judge_result.split("@@@@@")
    
        return answer, reason

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
