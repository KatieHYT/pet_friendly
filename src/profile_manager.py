import pandas as pd
import re
import os
import sys
import json
from datetime import datetime

from .tools import (
        get_file_contents,
        apify_crawl,
        get_review_info,
        save_reviews,
        save_string_to_file,
        read_json,
        )

class ProfileManager():
    def __init__(self, apify_api_key, raw_review_dir, filter_review_dir):
        self.apify_api_key = apify_api_key
        self.raw_review_dir = raw_review_dir
        self.filter_review_dir = filter_review_dir
        
    def _check_profile_exist(self, place_id):
        return place_id in os.listdir(self.raw_review_dir)
    
    def _get_newest_item(self, date_list):
        # Convert the list of date/time strings to datetime objects
        date_times = [datetime.strptime(date_str, "%Y_%m_%dT%H_%M_%S_%fZ") for date_str in date_list]

        # Get the newest datetime object using the max() function
        newest_item = max(date_times)

        return newest_item
    
    def _is_timeA_newer_than_timeB(self, timeA, timeB_dt):
        timeA_dt = datetime.strptime(timeA, "%Y_%m_%dT%H_%M_%S_%fZ")
#         timeB_dt = datetime.strptime(timeB, "%Y_%m_%dT%H_%M_%S_%fZ")

        # Compare the two datetime objects
        return timeA_dt > timeB_dt
    
    def _check_newer_review_exist(self, place_id, newest_dt_cloud):
        place_dir = os.path.join(self.raw_review_dir, place_id)
        datetime_list = []
        review_fns = os.listdir(place_dir)
        for _fn in review_fns:
            _datetime = _fn.split("Z_")[0] + "Z"
            datetime_list.append(_datetime)
        
        newest_dt_database = self._get_newest_item(datetime_list)

        return self._is_timeA_newer_than_timeB(timeA=newest_dt_cloud, timeB_dt=newest_dt_database)
    
    def seek_and_update(self, url_list):
        _review1 = apify_crawl(self.apify_api_key, url_list, max_reviews=1)
        _r1_place_id, _r1_datetime, _r1_review_id, _r1_place_name = get_review_info(_review1)
        print(f'place name: {_r1_place_name}')
        print(f'place id: {_r1_place_id}')
        if_profile_exist = self._check_profile_exist(_r1_place_id)
        if if_profile_exist:
            print('====profile exist')
            if_newer_r_exist = self._check_newer_review_exist(_r1_place_id, _r1_datetime)
            if if_newer_r_exist:
                print('======newer review exist on cloud')
                #TODO: how to properly set N_NEWEST 
                N_NEWEST=100
                self._go_apify(url, n_newest=N_NEWEST)
                self._filter_review(_r1_place_id)

            else:
                print('======no newer review on cloud')
        else:
            print('====profile not exist')
            reviews = apify_crawl(self.apify_api_key, url_list, max_reviews=100)
            save_reviews(reviews, self.raw_review_dir)
            self._filter_review(_r1_place_id)
        
        return _r1_place_id, _r1_datetime, _r1_review_id, _r1_place_name
    
    def _filter_review(self, _place_id):
        keyword_list = [
            'dog',
            'pet',
            'cat',
            'animal',
        ]
        place_dir = os.path.join(self.raw_review_dir, _place_id)
        review_fn_list = os.listdir(place_dir)
        for _review_fn in review_fn_list:
            review_path = os.path.join(place_dir, _review_fn)
            _review1 = read_json(review_path)
            review_text = _review1['text']
            place_id = _review1['placeId']
            datetime = _review1['publishedAtDate']
            print(datetime)
            datetime = datetime.replace("-", "_")
            datetime = datetime.replace(":", "_")
            datetime = datetime.replace(".", "_")
            print(datetime)
            review_id = _review1['reviewId']
            print(review_id)
            
            if review_text and any(word in review_text for word in keyword_list):
                print(review_text)
                save_dir = os.path.join(self.filter_review_dir, place_id)
                
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                save_path = os.path.join(save_dir, f'{datetime}_{review_id}.txt')
                save_string_to_file(save_path, review_text)

        
