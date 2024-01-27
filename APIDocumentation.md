## APIs Documentation
### Base URL
```bash
http://127.0.0.1:5000
```
### Endpoints 
#### 1) API to register a list of new users
```bash
POST /create
```
#### Response
Returns a JSON object with a list of created objects

#### Example
Request: 
```bash
POST http://127.0.0.1:5000/create
```
with body:
```bash
[
    {"full_name": "John", 
    "date_of_birth": "2004-02-27",
    "date_joined": "2023-08-16", 
    "date_left":"2024-01-01",
    "nric":"G1235432M",
    "department":"admin",
    "salary":2001.12,
    "remark":"None"},

    {"full_name": "Melissa", 
    "date_of_birth": "2002-03-28",
    "date_joined": "2022-08-16", 
    "nric":"G1335432U",
    "department":"admin",
    "salary":2001.12,
    "remark":"None"},

    {"full_name": "Gaia", 
    "date_of_birth": "2001-10-27",
    "date_joined": "2021-08-16", 
    "date_left":"2022-09-23",
    "nric":"G1235432L",
    "department":"admin",
    "salary":2001.12,
    "remark":"None"}
]
```
Response:
```bash
[
    "65b53c239894013f8c1a4d18",
    "65b53c249894013f8c1a4d1b",
    "65b53c249894013f8c1a4d1e"
]
```

#### 2) API to fetch data
```bash
GET /users
```
#### Response
Fetch employers' data from database with/without specified queries

#### Example
Request: 
```bash
GET http://127.0.0.1:5000/users
```

Response:
```bash
[{"_id": {"$oid": "65b53c239894013f8c1a4d18"}, "full_name": "John", "date_of_birth": "2004-02-27", "date_joined":
"2023-08-16", "date_left": "2024-01-01", "nric": "G1235432M", "department": "admin", "salary": 2001.12, "remark":
"None"}, {"_id": {"$oid": "65b53c249894013f8c1a4d1b"}, "full_name": "Melissa", "date_of_birth": "2002-03-28",
"date_joined": "2022-08-16", "nric": "G1335432U", "department": "admin", "salary": 2001.12, "remark": "None"}, {"_id":
{"$oid": "65b53c249894013f8c1a4d1e"}, "full_name": "Gaia", "date_of_birth": "2001-10-27", "date_joined": "2021-08-16",
"date_left": "2022-09-23", "nric": "G1235432L", "department": "admin", "salary": 2001.12, "remark": "None"}]
```

#### 3) API to update data
```bash
POST /users/<nric>
```
#### Response
Update data in database based on parameter "nric"

#### Example
Request: 
```bash
POST http://127.0.0.1:5000/users/G1235432M
```
with body
```bash
{
    "$set": {
    "department":"engineering",
    "salary":5200
    }
}
```
Response:
```bash
"Updated successfully!"
```

#### 4) API to delete data
```bash
DELETE /users/<nric>
```
#### Response
Delete data in database based on parameter "nric"

#### Example
Request: 
```bash
DELETE http://127.0.0.1:5000/users/G1235432M
```
Response:
```bash
"Employer removed successfully!"
```

#### 5) API to fetch log data
```bash
GET /read_log
```
#### Response
Fetch log data from database which stores timestamp and CUD (Create, Update, Delete) actions performed on each employer

#### Example
Request: 
```bash
GET http://127.0.0.1:5000/read_log
```
Response:
```bash
[{"_id": {"$oid": "65b53c249894013f8c1a4d1d"}, "timestamp": "2024-01-28 01:23:48.387241", "nric":
"G1235432L", "action": "create"}, {"_id": {"$oid": "65b5433d9894013f8c1a4d20"}, "timestamp": "2024-01-28
01:54:05.576015", "nric": "G1235432M", "action": "update"}, {"_id": {"$oid": "65b544149894013f8c1a4d22"}, "timestamp":
"2024-01-28 01:57:40.508936", "nric": "G1235432M", "action": "delete"}]
```
