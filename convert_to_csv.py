import csv
import json

import requests

def download_data(url: str) -> dict:
    '''
    Takes a URL as an input and returns the data we get from that URL
    '''
    data = json.loads(requests.get(url).text)
    return data

def get_countrycode_to_country_map(second_file_data) -> dict:
    '''
    Takes the countries file as input and returns the country_2_country_codes map
    '''
    country_2_country_codes = {}
    for country_code in second_file_data:
        if 'code' in country_code:
            country_2_country_codes[country_code['code']] = country_code['name']
    return country_2_country_codes

def process_record(rec: dict) -> dict:
    '''
    Takes the record and process the record to get the required fields
    '''
    new_rec = {}
    new_rec["_id"] = rec.get('id')
    new_rec["name"] = (rec.get('firstname', '') + ' ' + rec.get('surname', '')).strip()
    new_rec["dob"] = rec.get('born')
    prizes = rec.get('prizes', [])
    new_rec["unique_prize_years"] = ';'.join(list(set([i['year'] for i in prizes])))
    new_rec["unique_prize_categories"] = ';'.join(list(set([i['category'] for i in prizes])))
    if 'gender' in rec:
        new_rec["gender"] = rec.get('gender')
    new_rec["country"] = country_2_country_codes.get(rec.get('bornCountryCode'))
    return new_rec

def generate_csv():
    '''
    Generates a csv file by making the required processing for the input files
    '''
    # downloading the prizes file
    first_file_data = download_data('http://api.nobelprize.org/v1/laureate.json').get('laureates', [])
    # downloading the country file
    second_file_data = download_data('http://api.nobelprize.org/v1/country.json').get('countries', [])
    # getting the country codes map
    country_2_country_codes  = get_countrycode_to_country_map(second_file_data)
    # Creating a csv file
    csv_file = open('output_file.csv', 'w')
    csv_header = ['_id', 'name', 'dob', 'unique_prize_years', 'unique_prize_categories', 'gender', 'country']
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_header)
    for rec in first_file_data:
        new_rec = process_record(rec)
        csv_writer.writerow(new_rec.values())

    csv_file.close()
