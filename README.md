# Project Setup

# create environment
python3 -m venv env
# activate env
source env/bin/activate
or 
select python interpreter
# install requirements
pip install -r requirements.txt

# set env vars as per your creds
copy vars from .env.sample file and create new .env file.

# run migrations
./manage.py makemigrations

# run project
if env activated
./manage.py runserver

or 

after selecting python interpreter run django debugger