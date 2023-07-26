import os
from pprint import pprint
import openai

from tools import get_file_contents, save_string_to_file, read_json, talk2gpt

def check_store_attr(place_id):
    place_dir = os.path.join(raw_review_dir, place_id)
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
#             print(k)
#             print(_addit_info[k])
#         for _attr_dict in _addit_info[k]:
#             print(_attr_dict.keys())
#             for kk in _attr_dict.keys():
#                 if 'friendly' in kk:
#                     print(_attr_dict)
    return None


def gather_judge_input(guide_path, fn_path_list):
    guide = get_file_contents(guide_path)
    review_list = [get_file_contents(_fn) for _fn in fn_path_list]
    reviews = "\n".join(review_list)
    txt = guide + ': ' + reviews

    return txt


if __name__ == '__main__':
    raw_review_dir = './raw_review/'
    place_id_list = os.listdir(raw_review_dir)
    
    filter_review_dir = './filtered_review/'
    place_id_w_keyword_list = os.listdir(filter_review_dir)
    
    openai.api_key = get_file_contents('./api_key/openai')
    guide_path = './sample/guide.txt'
    
    place_id = place_id_list[0]
    
    # check the attribute that stores set by themselves on google map
    for _idx, place_id in enumerate(place_id_list):
        result = check_store_attr(place_id)
        if result is not None:
            print(result)
        else:
            # no review talk about it, return neutral
            if not (place_id in place_id_w_keyword_list):
                print('neutral')
            else: # ask ChatGPT to judge the review
                place_id_w_keyword_dir = os.path.join(filter_review_dir, place_id)
                fn_list = os.listdir(place_id_w_keyword_dir)
                fn_path_list = [os.path.join(place_id_w_keyword_dir, _fn) for _fn in fn_list]
                judge_input = gather_judge_input(guide_path, fn_path_list)
                judge_result = talk2gpt(judge_input)
                
                answer, reason = judge_result.split("@@@@@")

                print(answer)
