import requests
import asyncio
import time
from datetime import datetime
from flask import jsonify
from db import get_database_connection
from dotenv import load_dotenv
from os import environ

# Load environment variables from .env
load_dotenv()

YOUTUBE_API_KEY = environ.get('YOUTUBE_API_KEY')
YOUTUBE_API_URL = environ.get('YOUTUBE_API_URL')

# Get the database connection and cursor
db_conn, db_cursor = get_database_connection()

# Create the table if it does not exist
def initialize_table():
    create_query = """
    CREATE TABLE IF NOT EXISTS video_data (
        video_id VARCHAR(50) PRIMARY KEY,
        title TEXT,
        description TEXT,
        thumbnail_url TEXT,
        published_at DATETIME
    )
    """
    db_cursor.execute(create_query)
    db_conn.commit()

initialize_table()

# Function to query videos with pagination
def fetch_paginated_data(page_num):
    print(f"Fetching page {page_num} from database")
    page_size = 20
    offset = (int(page_num) - 1) * page_size

    select_query = "SELECT * FROM video_data ORDER BY published_at DESC LIMIT %s OFFSET %s"
    db_cursor.execute(select_query, (page_size, offset))
    records = db_cursor.fetchall()
    return jsonify(records)

# Function to perform search based on a keyword
def search_videos_by_keyword(keyword):
    print(f"Searching for videos with keyword: {keyword}")
    search_query = "SELECT * FROM video_data WHERE title LIKE %s OR description LIKE %s"
    wildcard_keyword = f"%{keyword}%"
    db_cursor.execute(search_query, (wildcard_keyword, wildcard_keyword))
    results = db_cursor.fetchall()
    return jsonify(results)

# Function to fetch the latest video data from YouTube API
async def fetch_latest_videos():
    print("Beginning video data retrieval from YouTube")
    page_token = ""

    while True:
        parameters = {
            "part": "snippet",
            "maxResults": 50,
            "type": "video",
            "key": YOUTUBE_API_KEY,
            "pageToken": page_token,
            "publishedAfter": "2020-01-01T00:00:00Z",
            "order": "date",
            "q": "Bollywood Music"
        }

        response = requests.get(YOUTUBE_API_URL, params=parameters)
        
        if response.status_code == 200:
            youtube_data = response.json()
            page_token = youtube_data.get('nextPageToken', '')

            video_list = []

            for item in youtube_data.get("items", []):
                video_id = item.get("id", {}).get("videoId")
                snippet = item.get("snippet", {})

                if snippet:
                    title = snippet.get('title')
                    description = snippet.get('description')
                    thumbnail_url = snippet.get('thumbnails', {}).get('default', {}).get('url')
                    publish_time_raw = snippet.get('publishTime')
                    publish_time = datetime.strptime(publish_time_raw, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')

                    video_entry = (video_id, title, description, thumbnail_url, publish_time)
                    video_list.append(video_entry)

            for video in video_list:
                time.sleep(1)  # Rate limiting
                db_cursor.execute("SELECT * FROM video_data WHERE video_id = %s", (video[0],))
                
                if db_cursor.fetchone() is None:
                    insert_query = """
                    INSERT INTO video_data (video_id, title, description, thumbnail_url, published_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    db_cursor.execute(insert_query, video)
                    db_conn.commit()
                    print(f"Inserted video with ID: {video[0]} into the database")
                else:
                    print(f"Video with ID: {video[0]} already exists")

        time.sleep(10)

# Start the process of video fetching
async def start_data_retrieval():
    await fetch_latest_videos()
