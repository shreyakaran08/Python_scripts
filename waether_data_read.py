import requests
import pandas as pd

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

def load_data(df, filename="weather_report.csv"):
    df.to_csv(filename, index=False)
    print(f"Pipeline complete! Data saved to {filename}")

def run_pipeline():
    # 1. Extract (Coordinates for NYC)
    raw_data = extract_weather_data(40.71, -74.00)
    
    if raw_data:
        # 2. Transform
        clean_df = transform_data(raw_data)
        
        # 3. Load
        load_data(clean_df)

if __name__ == "__main__":
    run_pipeline()




