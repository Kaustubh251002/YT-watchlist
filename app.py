
from flask import Flask, jsonify, request
from app.mongodb_controller import get_paginated_videos,save_videos_to_mongodb
from app.ytapi_controller import get_latest_videos
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/healthcheck', methods=['GET'])
def healthcheck_func():
    return "Service is up and running"

@app.route('/test',methods=['GET'])
def fetch_and_store_videos():
    query = "minecraft&dream|sapnap"
    videos = get_latest_videos(query)
    save_videos_to_mongodb(videos)
    return jsonify(videos)

@app.route('/videos', methods=['GET'])
def get_paginated_videos_route():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    videos = get_paginated_videos(page, per_page)
    return jsonify(videos)


if __name__ == '__main__':
    app.run(debug=True)