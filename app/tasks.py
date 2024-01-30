# app/tasks.py

from apscheduler.schedulers.background import BackgroundScheduler
from app.ytapi_controller import get_latest_videos
from app.mongodb_controller import save_videos_to_mongodb

def fetch_and_store_videos():
    query = "minecraft&dream|sapnap"
    videos = get_latest_videos(query)
    print("VIDEOS FETCHED!!")
    save_videos_to_mongodb(videos)
    print("VIDEOS INSERTED!!")

# Configure and start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_videos, trigger="interval", seconds=10)

