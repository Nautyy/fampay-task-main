# YouTube Video Data API

## Overview

This project provides a REST API to query and search video metadata retrieved from YouTube. It also periodically fetches new video data from the YouTube API and stores it in a MySQL database. It is built using Flask, Python, and MySQL.

## Features

- **Paginated Query**: Fetch video data with pagination.
- **Search Functionality**: Search for videos by title or description.
- **Data Fetching**: Retrieve latest video metadata from YouTube and store in MySQL.

## Technologies Used

- **Python** (3.10 or higher)
- **Flask** (for API server)
- **MySQL** (for storing video metadata)
- **YouTube Data API** (to fetch video details)

### Prerequisites
Ensure you have the following installed:
- Python 3.10 or later
- MySQL Server

### Getting Started
Follow these steps to set up and run the project locally:

1. Clone the Repository
```
git clone https://github.com/Nautyy/fampay-task-main.git
cd fampay-task-main
```
2. Set Up a Virtual Environment
Create and activate a virtual environment to manage project 
```
python -m venv venv
.\venv\Scripts\activate
```
3. Install the Requirements
Use the requirements.txt file to install necessary packages:

3. Install the Requirements
Use the requirements.txt file to install necessary packages:
`pip install -r requirements.txt`
4. Configure Environment Variables
Create a .env file in the root directory with the following content:
```
MYSQL_DATABASE='fampay'
MYSQL_USER='your_username'
MYSQL_PASSWORD='your_password'
MYSQL_HOST='localhost'
YOUTUBE_API_KEY='your_youtube_api_key'
YOUTUBE_API_URL='https://www.googleapis.com/youtube/v3/search/'
```

5. Set Up MySQL Database
Log into your MySQL server and setup the fampay database:
```
CREATE DATABASE fampay;
USE fampay;

CREATE TABLE ysearch (
    id VARCHAR(50) PRIMARY KEY,
    Title TEXT,
    Description TEXT,
    Thumbnails_urls TEXT,
    publishTime DATETIME
);
```

6. Run the Application `flask run`
You should see the server running at http://127.0.0.1:5000.

7. Start collecting the data in database
Visit the url `http://127.0.0.1:5000/initialise`


#### Output Screenshots : 

![ (2)](https://github.com/user-attachments/assets/2b7e1cfc-f28d-47be-98fb-7c9fe5b62cd3)
  
![ (1)](https://github.com/user-attachments/assets/b21ab686-3c70-44c0-8dbe-1f1f8801fea5)
![](https://github.com/user-attachments/assets/15d2fc5e-23f9-4841-9342-4575f3713dcf)
![(1)](https://github.com/user-attachments/assets/0ae90d87-25fd-4d8c-becb-db3896c5bd1b)
