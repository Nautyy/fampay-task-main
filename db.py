import mysql.connector
from dotenv import load_dotenv
from os import environ

# Load environment variables from the .env file
load_dotenv()

def get_database_connection():
    """
    Establishes and returns a connection to the MySQL database.
    """
    print('Initiating connection to MySQL...')
    try:
        conn = mysql.connector.connect(
            host=environ.get('MYSQL_HOST'),
            user=environ.get('MYSQL_USER'),
            password=environ.get('MYSQL_PASSWORD'),
            database=environ.get('MYSQL_DATABASE')
        )
        
        if conn.is_connected():
            print('Successfully connected to MySQL!')
            return conn, conn.cursor(dictionary=True)
    except mysql.connector.Error as err:
        print(f"Connection failed: {err}")
    
    return None, None
