from tools import get_file_contents
from apify_client import ApifyClient
from pprint import pprint
import os
import json


# TODO(yth):auto generate the following
url_list = [
{"url": "https://www.google.com/maps/place/La+Boulangerie+de+San+Francisco,+Hayes/@37.7765267,-122.4247172,17z/data=!4m6!3m5!1s0x808580a26e477b53:0xd9d0b8e2cce7c0dc!8m2!3d37.7767751!4d-122.4247997!16s%2Fm%2F04fhny7?hl=en&entry=ttu"},
{"url": "https://www.google.com/maps/place/Timbuk2/@37.7765798,-122.4254031,19.79z/data=!4m6!3m5!1s0x808580a26e69e867:0x9a0f2d8dc8ede28f!8m2!3d37.7768113!4d-122.4249217!16s%2Fg%2F1tv3nxrm?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Paolo+Shoes/@37.7765798,-122.4254031,19.79z/data=!4m6!3m5!1s0x808580a269502c91:0x812147579699341e!8m2!3d37.7767266!4d-122.4251618!16s%2Fg%2F1tlgy55m?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Archer+Nail+Bar/@37.7765798,-122.4254031,19.79z/data=!4m6!3m5!1s0x80858147c7c4b285:0x986146d744c66511!8m2!3d37.7768122!4d-122.4252174!16s%2Fg%2F11sgqz0f82?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Fiddlesticks/@37.7765798,-122.4254031,19.79z/data=!4m6!3m5!1s0x808580a26fb2afd3:0x7e5e7313d56a34b0!8m2!3d37.7766789!4d-122.4253417!16s%2Fg%2F1tfq4wqv?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Faherty+San+Francisco/@37.7766144,-122.4254136,20.07z/data=!4m6!3m5!1s0x8085818f1369ccfb:0x12f6f9e63a536335!8m2!3d37.7767607!4d-122.42542!16s%2Fg%2F11fmxj49s7?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Credo+Beauty/@37.7766532,-122.4254337,20.81z/data=!4m6!3m5!1s0x808581423acf8afb:0xfe85d671bde52e49!8m2!3d37.7767411!4d-122.4255301!16s%2Fg%2F11k61vmnbp?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/True+Sake/@37.7766532,-122.4254337,20.81z/data=!4m6!3m5!1s0x808580a2425a989b:0x7f8ab09ee61439fc!8m2!3d37.7766775!4d-122.4255577!16s%2Fg%2F1thvyhq5?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Orange+Bird/@37.7766151,-122.425734,20.81z/data=!4m6!3m5!1s0x808580a2434e46ff:0x2cc23ad6e7c43ee!8m2!3d37.7767427!4d-122.4256888!16s%2Fg%2F11gggg554q?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Buck+Mason/@37.7766096,-122.4258167,20.81z/data=!4m6!3m5!1s0x808581f74fb61b6d:0x934bc9aaad5b20ba!8m2!3d37.776724!4d-122.425781!16s%2Fg%2F11fnqwtrpv?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Cotton+Sheep/@37.7765951,-122.4259691,20.81z/data=!4m6!3m5!1s0x808580a27287425f:0x5c35c0c07b54a748!8m2!3d37.7766578!4d-122.4258269!16s%2Fg%2F1wh4g24g?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Salt+%26+Straw/@37.7765812,-122.4261254,20.81z/data=!4m6!3m5!1s0x808580a25b09718f:0x53cd2bf0f7e5e007!8m2!3d37.776618!4d-122.4260455!16s%2Fg%2F11g9ntm4ck?hl=en-US%27&entry=ttu"},

{"url": "https://www.google.com/maps/place/Gambit+Lounge/@37.7763517,-122.4260779,20.81z/data=!4m6!3m5!1s0x808581e3cfaa790f:0x541941460a82b90e!8m2!3d37.7763404!4d-122.4260054!16s%2Fg%2F11sbryvxh1?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Gioia+Pizzeria/@37.7764025,-122.4259918,21z/data=!4m6!3m5!1s0x8085818743a4ca0d:0xb199247306c93eab!8m2!3d37.7764094!4d-122.4258458!16s%2Fg%2F11h7dbp10c?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Metier/@37.7764025,-122.4259918,21z/data=!4m6!3m5!1s0x808580a24649fbb7:0xe4f22011be73370!8m2!3d37.7764252!4d-122.4257901!16s%2Fg%2F1tdl6btk?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/OAK+%2B+FORT/@37.7764057,-122.4259113,21z/data=!4m6!3m5!1s0x808580a2410629d1:0x96e69a0305f32506!8m2!3d37.7763173!4d-122.4256797!16s%2Fg%2F11c3swp5dh?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Nabilas+Natural+Foods/@37.7764057,-122.4259113,21z/data=!4m6!3m5!1s0x808580a243ce3a35:0x99a1bacf3ade6e78!8m2!3d37.7763347!4d-122.4256642!16s%2Fg%2F1tdcx9tz?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Outdoor+Voices/@37.7764338,-122.4258,21z/data=!4m6!3m5!1s0x808580a241c18db5:0x5bf9933f44e18084!8m2!3d37.7763709!4d-122.4256187!16s%2Fg%2F11f_j2gq7v?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Cotopaxi/@37.7764735,-122.4256276,21z/data=!4m6!3m5!1s0x808581f30d9262ef:0xab9d5e26b5c11615!8m2!3d37.7763834!4d-122.425524!16s%2Fg%2F11rdrjyjlk?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/SF+Dance+Gear/@37.7765244,-122.4254734,21z/data=!4m6!3m5!1s0x808f7fb390adcfff:0x37c04010b5c87fb2!8m2!3d37.7764186!4d-122.4254485!16s%2Fg%2F11f75yfn1c?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/RAILS+SAN+FRANCISCO/@37.7764921,-122.4253494,21z/data=!4m6!3m5!1s0x8085810ac7a5589d:0xe8b1340d7cc3591a!8m2!3d37.7763977!4d-122.4253243!16s%2Fg%2F11r97k6m_t?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Alla+Prima+Fine+Lingerie/@37.7764921,-122.4253494,21z/data=!4m6!3m5!1s0x808580a269852b89:0x6d5036ab27987e86!8m2!3d37.7763713!4d-122.4252593!16s%2Fg%2F1tj5qzj4?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Peak+Design+SF+Store/@37.7765048,-122.4252072,21z/data=!4m6!3m5!1s0x808f7fb9b3819f45:0xf309d4c3a5a588c4!8m2!3d37.776498!4d-122.425094!16s%2Fg%2F126020slf?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Brooklinen+San+Francisco/@37.7765048,-122.4252072,21z/data=!4m6!3m5!1s0x808581b6ddd65ce3:0xa8ec3c4278bd3679!8m2!3d37.7764239!4d-122.4250916!16s%2Fg%2F11p_0fnbw6?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Souvla/@37.7765048,-122.4252072,21z/data=!4m6!3m5!1s0x808580a26c77306d:0xb43108d1e99c8af1!8m2!3d37.776525!4d-122.4250028!16s%2Fg%2F1q5bmn70y?hl=en-US%27&entry=ttu"},
{"url": "https://www.google.com/maps/place/Patxi's+Pizza/@37.7765048,-122.4252072,21z/data=!4m6!3m5!1s0x808580a26da7c965:0x5cd5ff90503b0f97!8m2!3d37.7765207!4d-122.4248979!16s%2Fg%2F1jkxgv_yp?hl=en-US%27&entry=ttu"},

]
if __name__ == '__main__':

    # Initialize the ApifyClient with your API token
    api_key = get_file_contents('./api_key/apify')
    client = ApifyClient(api_key)
    
    # Prepare the actor input
    run_input = {
        "startUrls": url_list,
        "maxReviews": 100,
        "language": "en",
        "reviewsSort": "newest", 
    }
    
    # Run the actor and wait for it to finish
    run = client.actor("compass/google-maps-reviews-scraper").call(run_input=run_input)
    
    results = client.dataset(run["defaultDatasetId"]).iterate_items()
    
    for _id, _r in enumerate(results):
    
    #     print("="*100)
    #     pprint(_r)
    
        print('='*5, _id)
        place_id = _r['placeId']
        print(place_id)
        datetime = _r['publishedAtDate']
        print(datetime)
        datetime = datetime.replace("-", "_")
        datetime = datetime.replace(":", "_")
        datetime = datetime.replace(".", "_")
        print(datetime)
        review_id = _r['reviewId']
        print(review_id)
    
    
        review_dir = f'./raw_review/{place_id}'
        if not os.path.exists(review_dir):
            os.makedirs(review_dir)
        file = os.path.join(review_dir, f'{datetime}_{review_id}.json')
        with open(file, 'w') as f:
            json.dump(_r, f)
        
