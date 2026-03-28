import requests
import pandas as pd
import os
from dotenv import load_dotenv
import snowflake.connector
import json

# Load environment variables from .env file
load_dotenv()

def extract_weather_data(city_lat, city_long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city_lat}&longitude={city_long}&hourly=temperature_2m"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

def transform_data(raw_json):
    hourly_data = raw_json['hourly']
    df = pd.DataFrame(hourly_data)
    df['time']=pd.to_datetime(df['time'])
    df['temp'] = (df['temperature_2m'] - 32) * 5.0/9.0
    return df


def load_to_snowflake(df, table_name):
    # Read credentials from environment variables
    user = os.getenv('SNOWFLAKE_USER')
    password = os.getenv('SNOWFLAKE_PASSWORD')
    account = os.getenv('SNOWFLAKE_ACCOUNT')
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    database = os.getenv('SNOWFLAKE_DATABASE')
    schema = os.getenv('SNOWFLAKE_SCHEMA')
    
    # Validate that all required credentials are present
    required_vars = ['SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD', 'SNOWFLAKE_ACCOUNT', 
                     'SNOWFLAKE_WAREHOUSE', 'SNOWFLAKE_DATABASE', 'SNOWFLAKE_SCHEMA']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        return
    
    connection = None
    try:
        print(f"Connecting to Snowflake account: {account}")
        # Create connection using Snowflake connector
        connection = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        
        print(f"Connection successful. DataFrame shape: {df.shape}")
        print(f"DataFrame columns: {df.columns.tolist()}")
        print(f"Uploading to table: {table_name.upper()}")
        
        cursor = connection.cursor()
        
        # Create table if it doesn't exist
        columns_def = ', '.join([f"{col} VARCHAR" for col in df.columns])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name.upper()} ({columns_def})"
        cursor.execute(create_table_sql)
        
        # Insert data row by row
        rows_inserted = 0
        for idx, row in df.iterrows():
            values = ', '.join([f"'{str(val).replace(chr(39), chr(39)+chr(39))}'" if val is not None else 'NULL' for val in row])
            insert_sql = f"INSERT INTO {table_name.upper()} VALUES ({values})"
            cursor.execute(insert_sql)
            rows_inserted += 1
        
        connection.commit()
        print(f"Successfully uploaded {rows_inserted} rows to Snowflake table: {table_name}")
    except Exception as e:
        import traceback
        print(f"Error during Snowflake operation: {e}")
        traceback.print_exc()
    finally:
        if connection:
            connection.close()
            print("Connection closed")

# Main execution
if __name__ == "__main__":
    # Extract weather data for San Francisco (latitude: 37.7749, longitude: -122.4194)
    print("Extracting weather data for San Francisco...")
    raw_data = extract_weather_data(37.7749, -122.4194)
    
    if raw_data:
        # Transform the data
        print("Transforming data...")
        df = transform_data(raw_data)
        
        # Load to Snowflake
        print("Loading data to Snowflake...")
        load_to_snowflake(df, 'WEATHER_DATA')
    else:
        print("Failed to extract weather data")