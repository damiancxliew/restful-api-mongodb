### RESTful API Assessment with Python and MongoDB

This mini-project demonstrates how to design RESTful API with Python and MongoDB.

To retrieve the source of this project, you may clone this repository:

```bash
# Get the project code
git clone https://github.com/damiancxliew/restful-api-mongodb.git
```

##### Create your local environment on Anaconda (https://www.anaconda.com/download)
Open anaconda and enter the lines below to create a virtual environment:

```bash
conda create -n restfulapi python=3.11 anaconda # Create the environment
source activate restfulapi # Activate the environment
```

##### Install dependencies

```python
pip install -r requirements.txt
```

##### Install and start MongoDB Server

You may download and start MongoDB Server by following the steps below: https://linuxhint.com/start-mongodb-server-windows/. 

If you're using MacOS, you could use `brew` to start the server.

```bash
brew services start mongodb
```

#### Database schema
2 collections are being used in this project: "employer" and "log".
"Employer" is used to store employers' information while "log" is used for logging mechanism.
To faciliate data validation, the document structure is designed as such: 
```bash
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

``` 



#### Install Postman API Platform

You can install Postman through this link: https://www.postman.com/downloads/

##### Start the application

```bash
python run-app.py
```

Once the application is started, go to [localhost](http://localhost:5000/)
on Postman and explore the APIs.


#### Testcases

##### 1) Create


##### 1) Read


##### 1) Update


##### 1) Delete
