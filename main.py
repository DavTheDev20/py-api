# Full CRUD API created with MongoDB and FastAPI

import os
import sys
import traceback
import logging
from bson import ObjectId
from fastapi import Body, FastAPI, Response
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

try:
    MONGODB_URI = os.environ["MONGODB_URI"]
except KeyError:
    logging.exception("Please enter MONGODB_URI in .env file")
    sys.exit(1)

client = MongoClient(MONGODB_URI)

db = client['py-api-DB']
people = db['people']


@app.get('/people')
async def get_all_people(response: Response):
    """Gets all people from the database"""
    try:
        data = []
        for person in people.find({}):
            data.append({"_id": str(person['_id']), "first_name": person["first_name"],
                        "last_name": person["last_name"], "age": person["age"]})
        response.status_code = 200
        return {"success": True, "people": data}
    except:
        response.status_code = 500
        traceback.print_exc()
        return {"success": False, "error": traceback.format_exc()}


class Person(BaseModel):
    """Class designates schema for json request body"""
    first_name: str
    last_name: str
    age: int


@app.post('/people')
async def submit_post(response: Response, person: Person):
    """Creates new person and inserts them into the database"""
    try:
        new_person = {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "age": person.age
        }
        new_person_id = str(people.insert_one(new_person).inserted_id)
        response.status_code = 200
        return {"success": True, "person_id": new_person_id}
    except:
        response.status_code = 500
        return {"success": False, "error": traceback.format_exc()}


@app.get('/people/{person_id}')
async def get_single_person(response: Response, person_id: str):
    """Retrives single person with matching _id from database"""
    try:
        person_data = people.find_one({"_id": ObjectId(person_id)})
        person = {
            "_id": str(person_data["_id"]),
            "first_name": person_data["first_name"],
            "last_name": person_data["last_name"],
            "age": person_data["age"]
        }
        response.status_code = 200
        return {"success": True, "person": person}
    except TypeError:
        response.status_code = 400
        return {"success": False, "error": "Person with that _id does not exist"}
    except:
        response.status_code = 500
        traceback.print_exc()
        return {"success": False, "error": traceback.format_exc()}


@app.put('/people/{person_id}')
async def update_person(response: Response, person_id: str, person: Person):
    """Updates single person in database with matching _id"""
    try:
        person_updates = {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "age": person.age
        }
        result = people.replace_one(
            {"_id": ObjectId(person_id)}, person_updates).raw_result
        response.status_code = 200
        return {"success": True, "result": result}
    except:
        response.status_code = 400
        traceback.print_exc()
        return {"success": False, "error": traceback.format_exc()}


@app.delete('/people/{person_id}')
async def delete_person(response: Response, person_id: str):
    """Deletes single person in database with matching _id"""
    try:
        result = people.delete_one({"_id": ObjectId(person_id)}).raw_result
        response.status_code = 200
        return {"success": True, "result": result}
    except:
        response.status_code = 500
        traceback.print_exc()
        return {"success": False, "error": traceback.format_exc()}
