from flask import Flask
from dotenv import load_dotenv
from os import environ
import asyncio
from run import fetch_paginated_data, search_videos_by_keyword, start_data_retrieval

# Load the environment variables
load_dotenv()

app = Flask(__name__)

# Default route
@app.route("/")
def home():
    return "<h1>Welcome to the Video Search API</h1>"

# Route to fetch paginated video data
@app.route("/query")
@app.route("/query/<int:page>")
def get_videos(page=1):
    return fetch_paginated_data(page)

# Route to search for videos based on title or description
@app.route("/search")
@app.route("/search/<string:keyword>")
def search_videos(keyword=''):
    return search_videos_by_keyword(keyword)

# Route to start fetching video data from YouTube API
@app.route("/initialise")
def start():
    asyncio.run(start_data_retrieval())
    return "Video data retrieval has started!"

if __name__ == "__main__":
    app.run(debug=True)
