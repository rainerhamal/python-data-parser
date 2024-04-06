from dataclasses import field
import urllib.request
import zipfile
import os
import csv
import json
from datetime import datetime

url = 'https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip'
zip_filename = 'jodi_gas_csv_beta.zip'
extracted_filename = 'jodi_gas_csv_beta.csv'

# download file
def download_file(url, zip_filename):
    urllib.request.urlretrieve(url, zip_filename)

# unzipping file
def unzip_file(zip_filename, extract_dir = "."):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        return zip_ref.namelist()[0]
    
# read csv file
def parse_csv_to_json(csv_filename):
    with open(csv_filename, mode = 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            series_id = f"{row.get(list(row.keys())[0])}/{row.get(list(row.keys())[1])}"
            points = [[datetime.strptime(row['Date'], "%Y-%m-%d").isoformat(), float(row['Value'])]]
            fields = {key: row[key] for key in row.keys() if key not in ['Date', 'Value']}
    
            json_obj = {
                "series_id": series_id,
                "points": points,
                "fields": fields
            }
            print(json.dumps(json_obj))

def main():
    print("Downloading and extracting file...")
    download_file(url, zip_filename)
    csv_filename = unzip_file(zip_filename)

    print("Processing CSV data to JSON...")
    parse_csv_to_json(extracted_filename)

    os.remove(zip_filename)
    os.remove(csv_filename)

if __name__ == "__main__":
    main()
