FROM ubuntu:16.04
MAINTAINER James Matsumura (jmatsumura@som.umaryland.edu)

# Install SQLite/pip3/git
RUN apt-get update && apt-get install -y sqlite3 \
                                        python3-pip \
                                        git

# Get the Flask app
RUN git clone https://github.com/jmatsumura/flask_apps.git /home

WORKDIR /home/hospital_viewer

# Install python3 dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# Initialize and load the database
RUN ./initdb.py --schema hospitals.sql --load hospitals.json
# Expose port for Flask
EXPOSE 5000

CMD ["python3","./app.py"]