import json
import os

from tools import get_file_contents, save_string_to_file, read_json

#TODO(hyt): consult for keywords
keyword_list = [
    'dog',
    'pet',
    'cat',
    'animal',
]

if __name__ == '__main__':
    review_dir = './raw_review/'
    place_id_list = os.listdir(review_dir)
    for _place_id in place_id_list:
        place_dir = os.path.join(review_dir, _place_id)
        review_fn_list = os.listdir(place_dir)
        for _review_fn in review_fn_list:
            review_path = os.path.join(place_dir, _review_fn)
            _review1 = read_json(review_path)
            review_text = _review1['text']
            place_id = _review1['placeId']
            datetime = _review1['publishedAtDate']
    #         print(datetime)
            datetime = datetime.replace("-", "_")
            datetime = datetime.replace(":", "_")
            datetime = datetime.replace(".", "_")
            print(datetime)
            review_id = _review1['reviewId']
    #         print(review_id)
            
            if review_text and any(word in review_text for word in keyword_list):
                print(review_text)
                save_dir = f'./filtered_review/{place_id}'
                
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                save_path = os.path.join(save_dir, f'{datetime}_{review_id}.txt')
                save_string_to_file(save_path, review_text)
    
            
