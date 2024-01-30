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
            'channel_id': item['snippet']['channelId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'publish_datetime': item['snippet']['publishedAt'],
            'thumbnails': item['snippet']['thumbnails'],
            'channel_title': item['snippet']['channelTitle']
        }
        videos.append(video_info)
        
    return videos

def switch_to_next_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(yt_key)

def get_current_key():
    return yt_key[current_key_index]