# app/routes.py

from flask import Flask, jsonify, request
from app.mongodb_controller import get_paginated_videos

app = Flask(__name__)

@app.route('/videos', methods=['GET'])
def get_paginated_videos_route():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    videos = get_paginated_videos(page, per_page)
    return jsonify(videos)
