# app/mongodb_handler.py

from pymongo import MongoClient, UpdateOne
import os


mongodb_uri = os.environ.get('MONGO_URI')

client = MongoClient(mongodb_uri)
db = client['ytvids']
videos_collection = db['videos']

def save_videos_to_mongodb(videos):
    bulk_operations = []
    for video in videos:
        video_id = video['video_id']
        # Use upsert to insert or update based on the video_id
        bulk_operations.append(
            UpdateOne(
                    filter={'video_id': video_id},
                    update={'$set':{'video_id':video_id, 'title':video['title'], 'description': video['description'], 'publish_datetime':video['publish_datetime'], 'thumbnails':video['thumbnails']}},
                    upsert=True
            )    
        )
    # Execute the bulk operations
    if bulk_operations:
        videos_collection.bulk_write(bulk_operations)

def get_paginated_videos(page, per_page):
    # Calculate the skip value for pagination
    skip = (page - 1) * per_page

    # Retrieve paginated videos from the collection, sorted by publish datetime
    videos_cursor = videos_collection.find().sort('publish_datetime', -1).skip(skip).limit(per_page)

    print(videos_cursor)
    # Convert the cursor to a list of videos
    videos = list(videos_cursor)
    
    return videos