#! /usr/bin/env python3

"""
    A script to initialize an SQLite database which stores the following fields
    for hospital entries:

        id: integer identifier for the hospital
        name: name of the hospital
        city: city where the hospital is located
        state: two letter representation for the state the hospital is located in
        address: street address for the hospital

    Example usage:
        ./initdb.py --schema hospitals.sql --load hospitals.json

    Author: James Matsumura
"""

import sqlite3
import argparse
import json

def main():

    parser = argparse.ArgumentParser(description='Script to initialize and load an SQLite database with minimal hospital JSON data.')
    parser.add_argument('--db_name', '-db', default='hospitals.db', type=str, help='Path/name to SQLite DB.')
    parser.add_argument('--schema', '-s', required=True, type=str, help='Location of a SQLite schema file.')
    parser.add_argument('--load', '-l', required=True, type=str, help='Location of data to load the SQLite schema with.')
    args = parser.parse_args()

    try:
        cnx = sqlite3.connect(args.db_name)
        cur = cnx.cursor()

        with open(args.schema,'r') as initial_schema:
            sql = initial_schema.read()
            cnx.executescript(sql)

        hospital_data = None # store initial data from file here
        with open(args.load,'r') as initial_data:
            hospital_data = json.load(initial_data)
        
        for hospital in hospital_data:

            cur.execute(
                'INSERT INTO hospitals VALUES (?,?,?,?,?)',
                (
                    hospital['id'],
                    hospital['name'],
                    hospital['city'],
                    hospital['state'],
                    hospital['address']
                )
            )
        
        cnx.commit()

    except Exception as err:
        raise err
    
    else:
        cur.close()
        cnx.close()


if __name__ == '__main__':
    main()