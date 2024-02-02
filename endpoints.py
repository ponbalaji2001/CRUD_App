from flask_pymongo import pymongo
from flask import request
from flask import render_template
import urllib
import os
from dotenv import load_dotenv
load_dotenv()

#Connect MongoDB
con_string = os.getenv("MONGO_URI")
client = pymongo.MongoClient(con_string)

db = client.get_database('DemoDB')
user_collection = pymongo.collection.Collection(db, 'Demo')
print("...........................MongoDB connected Successfully.........................")

#GET Route
def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = render_template("index.html")
        #print("Hello")
        return res

    #Create the data in MongoDB (register data)
    @endpoints.route('/create', methods=['POST'])
    def create():
        res = {}
        try:
            req_body = request.json
            user_collection.insert_one(req_body)
            print("User data created successfully in database")
            status = {
                "statusCode": "200",
                "statusMessage": "User data created successfully in database"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        res['status'] = status
        return res

    #Update the data in MongoDB
    @endpoints.route('/update', methods=['PUT'])
    def update():
        res = {}
        try:
            req_body = request.json
            user_collection.update_one( {"id": req_body['id']}, {"$set": req_body['updated_user_body']})
            print("User data updated successfully in database")
            status = {
                "statusCode": "200",
                "statusMessage": "User data updated successfully in database"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        res['status'] = status
        return res

    #Read the data in MongoDB (retrieve data)
    @endpoints.route('/read', methods=['GET'])
    def read():
        res = {}
        try:
            users = user_collection.find({})
            users=list(users)
            res['data']=[{'Roll_no':user['roll_no'],'Name':user['name']}for user in users]
            status = {
                "statusCode": "200",
                "statusMessage": "User data retrieved successfully from database"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        res['status'] = status
        return res

    #Read the data by user name in MongoDB (retrieve data)
    @endpoints.route('/read/<name>', methods=['GET'])
    def readUser(name):
        res = {}
        try:
            users = user_collection.find_one({"name": name})
            res['data']=[{'Roll_no': users['roll_no'], 'Name':users['name']}]
            status = {
                "statusCode": "200",
                "statusMessage": "User data retrieved successfully from database"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        res['status'] = status
        return res

    #Delete the data in MongoDB
    @endpoints.route('/delete', methods=['DELETE'])
    def delete():
        res = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            print("User data deleted successfully in database")
            status = {
                "statusCode": "200",
                "statusMessage": "User data deleted successfully in database"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        res['status'] = status
        return res

    return endpoints
