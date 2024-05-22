import json

# Load JSON data from file with UTF-8 encoding
try:
    with open('jsondata.json', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)

    # Print the structure of the JSON data
    if isinstance(data, list):
        print(f"Total records: {len(data)}")
        if len(data) > 0:
            print("Sample record structure:")
            sample_record = data[0]
            for key, value in sample_record.items():
                print(f"{key}: {type(value).__name__} - {value}")
    else:
        print("The JSON data is not a list. Please provide a list of records.")

except FileNotFoundError:
    print("The file 'jsondata.json' was not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON data: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
