import json
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Function to parse dates
def parse_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, "%B, %d %Y %H:%M:%S")
        except ValueError:
            return None
    return None

# Load JSON data from file with UTF-8 encoding
try:
    with open('jsondata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Successfully loaded JSON data.")
except FileNotFoundError:
    print("The file 'jsondata.json' was not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON data: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred while loading JSON data: {e}")
    exit(1)

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Induja@11",
        database="datavisualizationnndb"
    )

    if conn.is_connected():
        print("Successfully connected to the database")

    cursor = conn.cursor()

    # Define the table creation query (if the table does not exist)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS insights (
        id INT AUTO_INCREMENT PRIMARY KEY,
        end_year VARCHAR(10),
        intensity INT,
        sector VARCHAR(100),
        topic VARCHAR(100),
        insight TEXT,
        url TEXT,
        region VARCHAR(100),
        start_year VARCHAR(10),
        impact VARCHAR(100),
        added DATETIME,
        published DATETIME,
        country VARCHAR(100),
        relevance INT,
        pestle VARCHAR(100),
        source VARCHAR(255),
        title TEXT,
        likelihood INT
    );
    """
    cursor.execute(create_table_query)
    print("Table 'insights' created or already exists.")

    # Define the insert query
    insert_query = """
    INSERT INTO insights (end_year, intensity, sector, topic, insight, url, region, start_year, impact, added, published, country, relevance, pestle, source, title, likelihood)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert data into the database
    for entry in data:
        try:
            cursor.execute(insert_query, (
                entry.get('end_year', None),
                int(entry['intensity']) if entry.get('intensity') else None,
                entry.get('sector', None),
                entry.get('topic', None),
                entry.get('insight', None),
                entry.get('url', None),
                entry.get('region', None),
                entry.get('start_year', None),
                entry.get('impact', None),
                parse_date(entry.get('added', None)),
                parse_date(entry.get('published', None)),
                entry.get('country', None),
                int(entry['relevance']) if entry.get('relevance') else None,
                entry.get('pestle', None),
                entry.get('source', None),
                entry.get('title', None),
                int(entry['likelihood']) if entry.get('likelihood') else None
            ))
        except Exception as e:
            print(f"Error inserting data: {entry}")
            print(e)

    # Commit the transaction
    conn.commit()
    print("Data committed to the database.")

    # Close the cursor and connection
    cursor.close()
    conn.close()
    print("Database connection closed.")

except Error as e:
    print(f"Database error: {e}")
    if conn.is_connected():
        cursor.close()
        conn.close()
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    if conn.is_connected():
        cursor.close()
        conn.close()
    exit(1)
