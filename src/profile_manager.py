import pandas as pd
import re
import os
import sys
import json
from datetime import datetime, timedelta

from .tools import (
        get_file_contents,
        apify_crawl,
        get_review_info,
        save_reviews,
        save_string_to_file,
        read_json,
        save_json,
        time_difference,
        make_latlng,
        )

class ProfileManager():
    def __init__(self, apify_api_key, raw_review_dir, filter_review_dir, last_update_dt_df_path, url2latlng_path):
        self.apify_api_key = apify_api_key
        self.raw_review_dir = raw_review_dir
        self.filter_review_dir = filter_review_dir
        
        self.last_update_dt_df_path = last_update_dt_df_path
        if not os.path.exists(last_update_dt_df_path):
            _df = {
                'latlng': [],
                'place_name': [],
                'last_update_dt': [],
            }
            self.last_update_dt_df = pd.DataFrame(_df)
        else:
            self.last_update_dt_df = pd.read_csv(last_update_dt_df_path)

        self.url2latlng_path = url2latlng_path
        if not os.path.exists(url2latlng_path):
            self.url2latlng = {}
        else:
            self.url2latlng = read_json(url2latlng_path)
        
    def _check_profile_exist(self, latlng):
        return latlng in os.listdir(self.raw_review_dir)
    
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
    
    def _check_newer_review_exist(self, latlng, newest_dt_cloud):
        place_dir = os.path.join(self.raw_review_dir, latlng)
        datetime_list = []
        review_fns = os.listdir(place_dir)
        for _fn in review_fns:
            _datetime = _fn.split("Z_")[0] + "Z"
            datetime_list.append(_datetime)
        
        newest_dt_database = self._get_newest_item(datetime_list)

        return self._is_timeA_newer_than_timeB(timeA=newest_dt_cloud, timeB_dt=newest_dt_database)

    def _check_is_freeze(self, latlng, freeze_mins):
        if latlng in list(self.last_update_dt_df['latlng']):
            _df = self.last_update_dt_df[self.last_update_dt_df['latlng']==latlng]
            previous_dt_str = _df['last_update_dt'].item()
            current_dt = datetime.now()
            current_dt_str = current_dt.strftime("%Y_%m_%dT%H_%M_%S_%fZ")
            time_diff = time_difference(current_dt_str, previous_dt_str)
            freeze_mins_delta = timedelta(minutes=freeze_mins)
            if time_diff < freeze_mins_delta:
                return True
            else:
                return False
        else:
            return False

    def _update_url2latlng(self, url_list):
        url = url_list[0]['url']
        _review1 = apify_crawl(self.apify_api_key, url_list, max_reviews=1)
        _, _r1_latest_review_dt, _, _r1_official_name, _r1_lat, _r1_lng = get_review_info(_review1)
        _r1_latlng = make_latlng(_r1_lat, _r1_lng)
        self.url2latlng[url] = _r1_latlng
        save_json(self.url2latlng, self.url2latlng_path)

        return _r1_latlng, _r1_latest_review_dt, _r1_official_name
    
    def _update_profile(self, url_list, _r1_latlng, _r1_datetime):
        if_profile_exist = self._check_profile_exist(_r1_latlng)
        if if_profile_exist:
            print('====profile exist')
            if_newer_r_exist = self._check_newer_review_exist(_r1_latlng, _r1_datetime)
            if if_newer_r_exist:
                print('======newer review exist on cloud')
                #TODO: how to properly set N_NEWEST 
                N_NEWEST=100
                reviews = apify_crawl(self.apify_api_key, url_list, max_reviews=N_NEWEST)
                save_reviews(reviews, self.raw_review_dir)
                self._filter_review(_r1_latlng)

            else:
                print('======no newer review on cloud')
        else:
            print('====profile not exist')
            reviews = apify_crawl(self.apify_api_key, url_list, max_reviews=100)
            save_reviews(reviews, self.raw_review_dir)
            self._filter_review(_r1_latlng)
    
    def check_and_update(self, url_list, freeze_mins):
        # TODO(kt):  this data format is to fit apify
        url = url_list[0]['url']
        # seek
        print("Checking...")
        is_in_url2latlng = False
        is_freeze = False
        if url in self.url2latlng.keys():
            is_in_url2latlng = True
            latlng = self.url2latlng[url]
            is_freeze = self._check_is_freeze(latlng, freeze_mins)

        print(f"In url2latlng? {is_in_url2latlng} ; Freeze now? {is_freeze}")
        if (not is_in_url2latlng) or (not is_freeze):
            print('Updating url2latlng...')
            latlng,  latest_review_dt, official_name = self._update_url2latlng(url_list)
            print('Updating profile...')
            self._update_profile(url_list, latlng, latest_review_dt)
            
            print('Updating last_update_dt_df...')
            # log a record into table
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y_%m_%dT%H_%M_%S_%fZ")
            # if already in log table, update
            if latlng in list(self.last_update_dt_df['latlng']):
                self.last_update_dt_df.loc[self.last_update_dt_df['latlng']==latlng, 'last_update_dt'] = current_time_str
            # if not in log table, add new row
            else:
                row = {
                    "latlng": latlng, 
                    "official_name": official_name,
                    "last_update_dt": current_time_str,
                }
                self.last_update_dt_df = self.last_update_dt_df.append(row, ignore_index=True)
            self.last_update_dt_df.to_csv(self.last_update_dt_df_path, index = False)
            print(f"Completed updating at {current_time}.")
      
        official_name = self.last_update_dt_df.loc[self.last_update_dt_df['latlng']==latlng, 'official_name'].item()
        print(f'place official name: {official_name}')
        print(f"LATLNG: {latlng}")
        return latlng, official_name
    
    def _filter_review(self, latlng):
        keyword_list = [
            'dog',
            'pet',
            'cat',
            'animal',
        ]
        place_dir = os.path.join(self.raw_review_dir, latlng)
        review_fn_list = os.listdir(place_dir)
        for _review_fn in review_fn_list:
            review_path = os.path.join(place_dir, _review_fn)
            _review1 = read_json(review_path)
            review_text = _review1['text']
            datetime = _review1['publishedAtDate']
            datetime = datetime.replace("-", "_")
            datetime = datetime.replace(":", "_")
            datetime = datetime.replace(".", "_")
            review_id = _review1['reviewId']
            
            if review_text and any(word in review_text for word in keyword_list):
                save_dir = os.path.join(self.filter_review_dir, latlng)
                
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                save_path = os.path.join(save_dir, f'{datetime}_{review_id}.txt')
                save_string_to_file(save_path, review_text)
