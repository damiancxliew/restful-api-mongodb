from flask import Flask, request, jsonify
from pymongo import MongoClient, ASCENDING
from bson.json_util import dumps
from urllib.parse import parse_qs
from jsonschema import validate
import datetime
import json
import ast


def parse_query_params(query_string): #Function to parse the query parameter string
    # Parse the query param string
    query_params = dict(parse_qs(query_string))
    # Get the value from the list
    query_params = {k: v[0] for k, v in query_params.items()}
    return query_params

def create_collection():
    client = MongoClient("mongodb://localhost:27017/") #connect to local host
    db = client["restfulapi_db"] #connect to db
    try:
        db.create_collection("employer")
    except Exception as e:
        print(e)

def validate_item(instance_dict): #data validation
    schema = {
    "type": "object",
    "properties": {
                "full_name": {
                    "type": "string",
                    "description": "must be a string and is required"
                },
                "date_of_birth": {
                    "type": "string",
                    "pattern": "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$",
                    "description": "must be a string and is required"
                    },
                "date_joined": {
                    "type": "string",
                    "pattern": "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$",
                    "description": "must be a date and is required"
                },
                "date_left": {
                    "type": "string",
                    "pattern": "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$",
                    "description": "must be a date and not required"
                },
                "nric": {
                    "type": "string",
                    "unique": True,
                    "description": "must be a string and is unique"
                },
                "department": {
                    "enum": ["admin", "engineering", "management", "sales", "qc"],
                    "description": "must be a string from the list"
                },
                "salary": {
                    "type": "number",
                    "description": "must be a float"
                },
                "remark": {
                    "type": "string",
                    "description": "must be a string"
                }
            },
    "required": ["full_name", "date_of_birth", "date_joined",\
                         "nric", "department", "salary", "remark"],
    }

    try:
        validate(instance=instance_dict, schema=schema) #data format is valid
        return True
    except: 
        return False
    
def log(nric, action): #Function to log data onto log_collection
    client = MongoClient("mongodb://localhost:27017/") #connect to local host
    db = client["restfulapi_db"] #connect to db
    log_coll = db["log"] #connect to log_collection
    log_coll.ensure_index([("timestamp", ASCENDING)]) 
    #insert into log
    log_coll.insert({"timestamp":str(datetime.datetime.now()), "nric":nric, "action": action})



create_collection()
client = MongoClient("mongodb://localhost:27017/") #connect to local host
db = client["restfulapi_db"] #connect to a db
employer_coll = db["employer"]

app = Flask(__name__)


@app.route("/create/", methods = ['POST'])
def create(): #Function to create new employer
    record_created = []
    try:
        body = ast.literal_eval(json.dumps(request.get_json()))
    except:
        return "", 400
    if isinstance(body, list):
        for item in body:
            if validate_item(item):
                query = {"nric":item["nric"]}
                if employer_coll.find(query).count() > 0:
                    return jsonify("NRIC is not unique!")
                else:
                    log(item["nric"], "create")
                    record_created.append(employer_coll.insert(item))
            else:
                return jsonify("Invalid input!")
            
    return jsonify([str(v) for v in record_created]), 201


@app.route("/users/", methods = ['GET'])
def read(): #Function to fetch employers' data
    try:
        # Call the function to get the query params
        query_params = parse_query_params(request.query_string)
        # Check if dictionary is not empty
        if query_params:
            # Try to convert the value to int
            query = {k.decode(): int(v) if isinstance(v, str) and v.isdigit() else v.decode() for k, v in query_params.items()}
            # Fetch all the record(s)
            records_fetched = employer_coll.find(query)

            # Check if the records are found
            if records_fetched.count() > 0:
                # Prepare the response
                return dumps(records_fetched)
            else:
                # No records are found
                return "", 404

        # If dictionary is empty
        else:
            # Return all the records as query string parameters are not available
            if employer_coll.find().count() > 0:
                # Prepare response if the users are found
                return dumps(employer_coll.find())
            else:
                # Return empty array if no users are found
                return jsonify([])
    except:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "", 500

    
@app.route("/users/<nric>", methods = ['POST'])
def update(nric): #Function to update employers' data
    try:
        # Get the value which needs to be updated
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "", 400

        # Updating the user

        records_updated = employer_coll.update_one({"nric": nric}, body)

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            log(nric, "update")
            return jsonify("Updated successfully!")
        else:
            # Bad request as the resource is not available to update
            # Add message to show invalid NRIC
            return jsonify("Invalid input!")
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500

    
@app.route("/users/<nric>", methods = ['DELETE'])
def delete(nric): #Function to remove employer
    try:
        # Delete the user
        delete_user = employer_coll.delete_one({"nric": nric})

        if delete_user.deleted_count > 0 :
            # Prepare the response
            log(nric, "delete")
            return jsonify("Employer removed successfully!")
        else:
            # Resource Not found
            return jsonify("Invalid input!")
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/read_log/", methods = ['GET'])
def read_log():
    log_coll = db["log"]
    try:
        return dumps(log_coll.find())
    except:
        return jsonify("Error!")
    

@app.errorhandler(404)
def page_not_found(e):
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer to API documentation."
            }
    }
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp



if __name__ == '__main__':
    app.run(debug=False)
