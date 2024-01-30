from googleapiclient.discovery import build
import os,time
from dotenv import load_dotenv

load_dotenv()

yt_key = os.environ.get('YOUTUBE_API_KEY').split(',')
current_key_index = 0


def get_latest_videos(query):
    
    youtube = build('youtube', 'v3', developerKey=get_current_key())
    
    for attempt in range(3):
        request = youtube.search().list(
            q=query,
            part='id,snippet',
            order='date',
            type='video',
            maxResults=10  # Adjust the number of results as needed
        )
        response = request.execute()
        if response.status_code == 200:
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
            
        elif response.status_code == 403 and "rateLimitExceeded" in response.text:
            #Using exponential backoff to wait for a period before retrying
            wait_time = (2 ** attempt)
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds.")
            time.sleep(wait_time)
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    #Breaking out of the loop implies failure in retreiving  data from current api key
    switch_to_next_key()
    #Use the new key to return data
    get_latest_videos(query)
    

def switch_to_next_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(yt_key)

def get_current_key():
    return yt_key[current_key_index]