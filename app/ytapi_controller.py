from googleapiclient.discovery import build
import os

yt_key = os.environ.get('YOUTUBE_API_KEY')

def get_latest_videos(query):
    
    videos = []
    
    return videos