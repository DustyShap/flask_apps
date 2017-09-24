# hospital_viewer

A simple RESTful Python Flask app to view hospital records following [this format](https://raw.githubusercontent.com/incompass/coding-challenge-assets/master/hospitals.json).

* [Setup](https://github.com/jmatsumura/flask_apps/tree/master/hospital_viewer#setup)
  * [Ubuntu](https://github.com/jmatsumura/flask_apps/tree/master/hospital_viewer#ubuntu-tested-with-ubuntu-1604--python-35)
  * [Docker](https://github.com/jmatsumura/flask_apps/tree/master/hospital_viewer#docker)
* [Usage](https://github.com/jmatsumura/flask_apps/tree/master/hospital_viewer#usage)
  * [Endpoints](https://github.com/jmatsumura/flask_apps/tree/master/hospital_viewer#endpoints)

## Setup

### Ubuntu (tested with Ubuntu 16.04 + Python 3.5)

**Note**: You may want to use a [virtual environment](https://docs.python.org/3/library/venv.html) to separate these installs from others. 

1. Install all the Python3 dependencies found in [requirements.txt](https://github.com/jmatsumura/flask_apps/blob/master/hospital_viewer/requirements.txt)
  * `pip install -r requirements.txt`
2. Install sqlite3
  * `sudo apt install sqlite3`
3. Initialize the SQLite database and populate with some data (point these arguments to the files downloaded at the root of this repository). 
  * `./initdb.py --schema hospitals.sql --load hospitals.json`
4. Start up the Flask application (will be visible at localhost:5000 unless a new [configuration file](http://flask.pocoo.org/docs/0.12/config/) is set via the `CUSTOM_FLASK_CONF` environmental variable).
  * `./app.py`
5. Verify the application/database are properly up and running.
  * `tests/test_app.py`

### Docker

1. Use the Dockerfile at the root of the repository to build the image OR use docker pull (pulls from [this](https://hub.docker.com/r/jmatsumura/hospital-viewer/) Docker image).
  * `docker build -t jmatsumura/hospital-viewer .`
  * `docker pull jmatsumura/hospital-viewer`
2. Run the image and map your chosen port (using 8888 here).
  * `docker run -d -p 8888:5000 jmatsumura/hospital-viewer`
3. Can visit the site at a location given the previous port like `localhost:8888`.

## Usage

Runs by default on port 5000 and hosts on 0.0.0.0 so can be reached by any of:
* `localhost:5000`
* `127.0.0.1:5000`
* `0.0.0.0:5000`

### Endpoints:
* `~/`
  * Root of the site which will render all the current hospital entries stored in the database. Uses the GET route of `~/hospitals` to obtain this information.

* `~/hospitals`
  * Can be used via GET without any following value to pull all hospitals in JSON format. One can also access an individual hospital's data by ID by following this endpoint with the desired ID (e.g. `~/hospitals/1`). This endpoint also allows POST requests. One can add new hospital entries through a POST request on the `~/hospitals` endpoint providing a JSON list which follows the structure of https://raw.githubusercontent.com/incompass/coding-challenge-assets/master/hospitals.json. For example, one can use a command such as `curl` to add entries:

`curl -H "Content-Type: application/json" -X POST -d '[{"hospital":"data","not":"valid"}]' http://localhost:5000/hospitals`

or instead of putting the content in the terminal the data can be sent via a properly formatted file like:

`curl -H "Content-Type: application/json" -X POST --data-binary @/path/to/new_hospitals.json http://localhost:5000/hospitals`

