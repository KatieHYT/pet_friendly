import json
import os
import openai
from apify_client import ApifyClient

def get_file_contents(filename):
    """ 
    src: https://github.com/dylburger/reading-api-key-from-file/blob/master/Keeping%20API%20Keys%20Secret.ipynb
        Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

def save_string_to_file(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
        print("String successfully saved to file.")
    except Exception as e:
        print(f"Error occurred while saving the string: {e}")

def read_json(f_path):
   with open(f_path, 'r') as f:
       data = json.load(f)

   return data

def talk2gpt(txt, if_stream=False):
    msg = {
        "role": "user",
        "content": txt,
         #"temperature": 0.7,
    #     "top_p": 0.1,
        "name": "cradle",
    }

    # create a chat completion
    # TODO: stream the chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            msg
        ],
        stream=if_stream,
    #     temperature=1,
    #     top_p=0.1,
    #     n=3,
    )
    
    if if_stream:
        return chat_completion
    else:
        return chat_completion.choices[0].message.content

    
def remove_empty_lines(input_string):
    lines = input_string.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def apify_crawl(api_key, url_list, max_reviews, reviews_sort="newest"):
    client = ApifyClient(api_key)
    # Prepare the actor input
    run_input = {
        "startUrls": url_list,
        "maxReviews": max_reviews,
        "language": "en",
        "reviewsSort": reviews_sort,
    }
    # Run the actor and wait for it to finish
    run = client.actor("compass/google-maps-reviews-scraper").call(run_input=run_input)
    results = client.dataset(run["defaultDatasetId"]).iterate_items()
    
    return results

def get_review_info(reviews):
    for _id, _r in enumerate(reviews):
        place_id = _r['placeId']
        datetime = _r['publishedAtDate']
        datetime = datetime.replace("-", "_")
        datetime = datetime.replace(":", "_")
        datetime = datetime.replace(".", "_")
        review_id = _r['reviewId']
        place_name = _r['title']

    return place_id, datetime, review_id, place_name

def save_reviews(reviews, raw_review_dir):
    for _id, _r in enumerate(reviews):
        place_id = _r['placeId']
        datetime = _r['publishedAtDate']
        datetime = datetime.replace("-", "_")
        datetime = datetime.replace(":", "_")
        datetime = datetime.replace(".", "_")
        review_id = _r['reviewId']

        review_dir = os.path.join(raw_review_dir, place_id)
        if not os.path.exists(review_dir):
            os.makedirs(review_dir)
        file = os.path.join(review_dir, f'{datetime}_{review_id}.json')
        with open(file, 'w') as f:
            json.dump(_r, f)

def extract_place_name_lat_lng(url):
#     url = 'https://www.google.com/maps/place/Credo+Beauty/@37.7767411,-122.4255301,17z/data=!3m1!4b1!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp?hl=en-TW&entry=ttu'
#     url = 'https://www.google.com/maps/place/Credo+Beauty/@37.7767411,-122.4255301,19z/data=!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp?entry=ttu '
#     url = 'https://www.google.com/maps/place/Credo+Beauty,+552+Hayes+St,+San+Francisco,+CA+94102/@37.7767411,-122.4255301,19z/data=!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp'
#     url = 'https://www.google.com/maps/place/Credo+Beauty/@37.7764595,-122.4255926,20.1z/data=!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp?entry=ttu'
# # place_name, lat, lng = extract_place_name_lat_lng(url)
    _store_name, _lattitude, _longitude = re.search(r'/maps/place/(.*?)/@(.*?),(.*?),', url).groups()
    store_name = _store_name.split(',')[0]
    lattitude = float(_lattitude)
    longitude = float(_longitude)
    
    return store_name, lattitude, longitude
