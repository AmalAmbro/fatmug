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


# API Endpoints

# USER
# created user via createsuper or from admin
url: http://127.0.0.1:8000/api/users/login/
method: POST

payload
username:<string>
password:<string>

response
token: <string>

# VENDOR
# list
url: http://127.0.0.1:8000/api/vendors/
authorization: Token <token string>
method: GET

response:
pagination and array of results


# detail
url: http://127.0.0.1:8000/api/vendors/id/
authorization: Token <token string>
method: GET

response:
json serialized details


# create
url: http://127.0.0.1:8000/api/vendors/
authorization: Token <token string>
method: POST

payload:
name:Blakeboris
contact_details:8475599393
address:BLAKE enterprises pvt ltd , Ekm Jn P.O
vendor_code:89384
on_time_delivery_rate:0
quality_rating_avg:0
average_response_time:0
fulfillment_rate:0

response:
json serialized details


# update
url: http://127.0.0.1:8000/api/vendors/id/
authorization: Token <token string>
method: PUT

payload:
name:Blakeboris
contact_details:8475599393
address:BLAKE enterprises pvt ltd , Ekm Jn P.O
vendor_code:89384
on_time_delivery_rate:0
quality_rating_avg:0
average_response_time:0
fulfillment_rate:0

response:
json serialized details

# delete
url: http://127.0.0.1:8000/api/vendors/id/
authorization: Token <token string>
method: DELETE


# Purchase Order
# list
url: http://127.0.0.1:8000/api/purchase_orders/
authorization: Token <token string>
method: GET

response:
pagination and array of results

# detail
url: http://127.0.0.1:8000/api/purchase_orders/id/
authorization: Token <token string>
method: GET

response:
json serialized detail

# create
url: http://127.0.0.1:8000/api/purchase_orders/
authorization: Token <token string>
method: POST

payload:
po_number:938822
vendor:3
order_date:2024-04-30T12:04:00
delivery_date:2024-05-01T07:58:00
items:["handbar", "axle"]
quantity:50
issue_date:2024-04-30T11:58:00

response:
json serialized detail

# update
url: http://127.0.0.1:8000/api/purchase_orders/id/
authorization: Token <token string>
method: PUT

po_number:565555
vendor:3
order_date:2024-04-30T12:04:00Z
delivery_date:2024-05-10T11:58:00Z
items:["handbar", "axle"]
quantity:50
quality_rating:4.7
issue_date:2024-05-04T11:58:00Z
status:completed

response:
json serialized data


# delete
url: http://127.0.0.1:8000/api/purchase_orders/id/
authorization: Token <token string>
method: DELETE

# acknowledgment
url: http://127.0.0.1:8000/api/purchase_orders/5/acknowledge/
authorization: Token <token string>
method: PUT

payload:
acknowledgment_date:2024-04-29T17:28:00Z

response:
json serialized detail
