import os
import json

from tools import get_file_contents, save_string_to_file, read_json

if __name__ == '__main__':
    raw_review_dir = './raw_review/'
    place_id_list = os.listdir(raw_review_dir)
    
    filter_review_dir = './filtered_review/'
    place_id_w_keyword_list = os.listdir(filter_review_dir)
    
    guide_path = './sample/guide.txt'
    
    place_id = place_id_list[0]
    
    storeid2storename_map = {}
    for _idx, place_id in enumerate(place_id_list):
        place_dir = os.path.join(raw_review_dir, place_id)
        review_id_list = os.listdir(place_dir)
        fn = review_id_list[0]
        file_path = os.path.join(place_dir, fn)
    
        # apify save store info into every review, so we only parse the first one
        _review1 = read_json(file_path)
        
        place_name = _review1['title']
        storeid2storename_map[place_id] = place_name
    
        map_path = f'./storeid2storename_map.json'
        with open(map_path, 'w') as f:
            json.dump(storeid2storename_map, f)
