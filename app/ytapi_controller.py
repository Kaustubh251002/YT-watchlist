from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

yt_key = os.environ.get('YOUTUBE_API_KEY').split(',')


def get_latest_videos(query):
    
    youtube = build('youtube', 'v3', developerKey=yt_key[0])

    # Make a search request to get the latest videos
    request = youtube.search().list(
        q=query,
        part='id,snippet',
        order='date',
        type='video',
        maxResults=10  # Adjust the number of results as needed
    )

    response = request.execute()

    # Extract relevant information from the API response
    videos = []
    for item in response.get('items', []):
        video_info = {
            'video_id': item['id']['videoId'],
            # 'title': item['snippet']['title'],
            # 'description': item['snippet']['description'],
            # 'publish_datetime': item['snippet']['publishedAt'],
            # 'thumbnails': item['snippet']['thumbnails']
        }
        videos.append(video_info)
        
    return videos