import os
from pdb import Restart
import traceback
from fastapi import Body, FastAPI, Response, status
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = FastAPI()
client = MongoClient(os.environ["MONGODB_URI"])

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
        return {"success": False, "error": traceback.format_exc()}


@app.post('/people')
async def submit_post(req_body: dict = Body(...)):
    try:
        new_person = req_body
        new_person_id = str(people.insert_one(new_person).inserted_id)
        print(new_person_id)
    except:
        return traceback.format_exc()
