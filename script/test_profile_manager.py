import sys 

sys.path.append("..")
from src.profile_manager import ProfileManager
from src.tools import get_file_contents, apify_crawl, get_review_info, save_reviews

if __name__ == '__main__':
    # url = 'https://www.google.com/maps/place/Credo+Beauty/@37.7767411,-122.4255301,17z/data=!3m1!4b1!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp?hl=en-TW&entry=ttu'
    # url = 'https://www.google.com/maps/place/Credo+Beauty/@37.7767411,-122.4255301,19z/data=!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp?entry=ttu '
#     url = 'https://www.google.com/maps/place/Credo+Beauty,+552+Hayes+St,+San+Francisco,+CA+94102/@37.7767411,-122.4255301,19z/data=!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp'
#     url = 'https://www.google.com/maps/place/Credo+Beauty/@37.7764595,-122.4255926,20.1z/data=!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp?entry=ttu'
#     url = 'https://www.google.com/maps/place/Peak+Design+SF+Store/@37.776498,-122.4276689,17z/data=!3m1!4b1!4m6!3m5!1s0x808f7fb9b3819f45:0xf309d4c3a5a588c4!8m2!3d37.776498!4d-122.425094!16s%2Fg%2F126020slf?hl=en-TW&entry=ttu'
    url = 'https://www.google.com/maps/place/Cotopaxi,+549+Hayes+St,+San+Francisco,+CA+94102,+United+States/@37.7763834,-122.425524,16z/data=!4m6!3m5!1s0x808581f30d9262ef:0xab9d5e26b5c11615!8m2!3d37.7763834!4d-122.425524!16s%2Fg%2F11rdrjyjlk?hl=en-TW&gl=tw'
    
    url_list = [{'url': url}]
    raw_review_dir = './test_raw_review'
    
    api_key = get_file_contents('/TOP/home/kt/API_KEY/apify')
    pm = ProfileManager(apify_api_key=api_key, raw_review_dir='./test_raw_review/')
    _r1_place_id, _r1_datetime, _r1_review_id, _r1_place_name = pm.seek_and_update(url_list)
    
    print(_r1_place_name)
    print(_r1_place_id)
