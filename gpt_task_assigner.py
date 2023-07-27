import openai
import json

from .pet_friendly_judger import PetFriendlyJudger
from .tools import read_json

class GPTTaskAssigner():
    def __init__(self, api_key):
        openai.api_key = api_key
        self.pfj = PetFriendlyJudger()

    def chat(self, input_msg):
        return talk2gpt(input_msg)

    def judge_store_pet_friendly(self, input_msg):
        
        #TODO(hyt): the following is a temporary solution before we include latitude and lontitude
        # START
        _map = read_json('/TOP/home/kt/DATA/cradle/google_review/storeid2storename_map.json')
        name_list = []
        _map_rev = {}
        for k, v in _map.items():
            name_list.append(v)
            _map_rev[v] = k
        import difflib
        matches = difflib.get_close_matches(input_msg, name_list, cutoff=0.1)
        print(matches)
        store_name = matches[0]
        place_id = _map_rev[store_name]
        #### END


        answer, reason = self.pfj.judge_store(place_id)

        content = f"{store_name}'s pet-friendly status might be {answer} {reason}"

        return content
