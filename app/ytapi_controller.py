from googleapiclient.discovery import build
import os,time
from dotenv import load_dotenv

load_dotenv()

yt_key = os.environ.get('YOUTUBE_API_KEY').split(',')
current_key_index = 0
response=None

def get_latest_videos(query):
    
    youtube = build('youtube', 'v3', developerKey=get_current_key())
    
    for attempt in range(3):
        request = youtube.search().list(
            q=query,
            part='id,snippet',
            order='date',
            type='video',
            maxResults=10  
        )
        try:
            global response
            response = request.execute()
            return handle_success(response)
        except Exception as e:
            print (e)

            # <HttpError 403 when requesting https://youtube.googleapis.com/youtube/v3/search?q=minecraft%26dream%7Csapnap&part=id%2Csnippet&order=date&type=video&maxResults=10&key=AIzaSyA-ShXE0S2uEp3-BqS8Tw6sMw-l2ZKg82g&alt=json returned "The request cannot be completed because you have exceeded your <a href="/youtube/v3/getting-started#quota">quota</a>.". Details: "[{'message': 'The request cannot be completed because you have exceeded your <a href="/youtube/v3/getting-started#quota">quota</a>.', 'domain': 'youtube.quota', 'reason': 'quotaExceeded'}]">
            # catch this error
            if e.resp.status in [403, 500, 503]:
                #Using exponential backoff to wait for a period before retrying
                wait_time = (2 ** attempt)
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds.")
                time.sleep(wait_time)
                attempt+=1
            
            
    #Breaking out of the loop implies failure in retreiving  data from current api key
    switch_to_next_key()
    #Use the new key to return data
    get_latest_videos(query)
    
def handle_success(response):
    videos = []
    for item in response.get('items', []):
        video_info = {
            'video_id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'publish_datetime': item['snippet']['publishedAt'],
            'thumbnails': item['snippet']['thumbnails']
        }
        videos.append(video_info)
        
    return videos

def switch_to_next_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(yt_key)

def get_current_key():
    return yt_key[current_key_index]