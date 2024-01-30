
from flask import Flask, jsonify, request
from app.mongodb_controller import get_paginated_videos,save_videos_to_mongodb
from app.ytapi_controller import get_latest_videos
from dotenv import load_dotenv
from app.tasks import scheduler


load_dotenv()

app = Flask(__name__)

#Debug route to check service status
@app.route('/healthcheck', methods=['GET'])
def healthcheck_func():
    return "Service is up and running!!"
#GET route to fetch data for user
@app.route('/videos', methods=['GET'])
def get_paginated_videos_route():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    videos = get_paginated_videos(page, per_page)
    return videos


if __name__ == '__main__':
    try:
        scheduler.start()
        app.run(debug=True)
    finally:
        scheduler.shutdown()