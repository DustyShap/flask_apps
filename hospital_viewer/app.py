#! /usr/bin/env python3

"""
    A Flask app which renders a base set of hospital data stored in an SQLite
    database.

    Runs by default on port 5000 and hosting 0.0.0.0 so can be reached by any of:
        localhost:5000
        127.0.0.1:5000
        0.0.0.0:5000

    Endpoints:
    ~/
        Root of the site and will render all the current hospital entries stored
        in the database. Uses the GET route of ~/hospitals to obtain this 
        information.

    ~/hospitals
        Can be used via GET without any following value to pull all hospitals. 
        One can also access individual hospitals by ID by following this 
        endpoint with the desired ID (e.g. ~/hospitals/1). POST can be used 
        on the base endpoint providing a JSON list which follows the structure of
        https://raw.githubusercontent.com/incompass/coding-challenge-assets/master/hospitals.json

    Author: James Matsumura
"""

from flask import Flask, jsonify, request, render_template, url_for
import json
import os
import sqlite3

app = Flask(__name__) # setup the Fask app
app.config.from_object(__name__) # load local conf and set defaults
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'hospitals.db')
))
app.config.from_envvar('CUSTOM_FLASK_CONF', silent=True) # can add custom conf if desired

#############
# ENDPOINTS #
#############

@app.route('/', methods=['GET'])
def render_hospitals():
    """
    Root of the site which displays all hospitals present in SQLite DB.
    """

    all_hospitals = (json.loads(get_hospitals().response[0]))
    return render_template('display_hospitals.html', hospital_list=all_hospitals)

@app.route('/hospitals', methods=['GET','POST']) # no ID yields all IDs
@app.route('/hospitals/<int:hospital_id>', methods=['GET']) # return a single hospital record
def get_hospitals(hospital_id=None):
    """
    Both the GET and POST endpoint for retrieving and uploading new hospital 
    information.

    Args:
        hospital_id: append ~/hospitals/ with an int (e.g. ~/hospitals/1) to 
        view that particular ID's entry data. 
    """

    if request.method == 'GET':

        try:
            cnx = sqlite3.connect(app.config['DATABASE'])
            cur = cnx.cursor()

            if not hospital_id or hospital_id == 'all':

                cur.execute("SELECT * FROM hospitals ORDER BY ID")

                hospital_list = [] # build this from each row returned in DB

                for row in cur:
                    hospital_list.append(build_hospital_entry_from_sqlite(row))

                return jsonify(hospital_list)

            elif isinstance(hospital_id, int):

                cur.execute("SELECT * FROM hospitals WHERE ID=?", (hospital_id,))
                res = cur.fetchone()

                if res:
                    return jsonify(build_hospital_entry_from_sqlite(res))

                else: # return a notifcation when there is no entry in the database
                    response = jsonify({'message': 'No hospital with ID = {}'.format(hospital_id)})
                    response.status_code = 200

                    return response

        except Exception as err:
            raise err
        
        else:
            cur.close()
            cnx.close()

    else: # handling POST for new hospital record uploads

        conflicting_keys,incorrect_format = ([] for i in range(2))
        minimal_data = set(['id','name','city','state','address'])

        try:
            cnx = sqlite3.connect(app.config['DATABASE'])
            cur = cnx.cursor()

            for hospital in request.get_json():

                keys = hospital.keys()

                # A lot of additional error handling beyond the following checks
                # could be added here like enforcing valid/harmonized IDs, 
                # names, cities, states, and addresses.
                if len(keys) != len(set(keys)): # too many keys
                    incorrect_format.append(hospital)
                    continue

                elif minimal_data != set(hospital.keys()): # wrong set of keys
                    incorrect_format.append(hospital)
                    continue

                try:
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

                except Exception as err: # failed the PK constraint on ID
                    conflicting_keys.append(hospital['id'])

            db_update_msg = (
                "Any ID values present in conflicting_keys mean the entity's "
                "ID already exist in the database so they must be changed before "
                "uploading. Any entries in incorrect_format do not have the "
                "required minimal data for a hospital upload (id, name, city, "
                "state, address) or the data is ill-formatted."
            )

            response = jsonify({
                'conflicting_keys': conflicting_keys, 
                'incorrect_format': incorrect_format, 
                'message': db_update_msg}
            )
            response.status_code = 200

            return response

        except Exception as err:
            raise err
        
        else:
            cur.close()
            cnx.close()


#############
# FUNCTIONS #
#############

def build_hospital_entry_from_sqlite(row):
    """
    Builds a complete dict of the hospital entry from the 5 columns returned
    from a hospital entry in the SQLite database.
    
    Args:
        row: of data from SQLite hospitals table. 
    """  

    hospital_entry = {
        'id': row[0],
        'name': row[1],
        'city': row[2],
        'state': row[3],
        'address': row[4]
    }

    return hospital_entry


if __name__ == '__main__':
    app.run(host='0.0.0.0')