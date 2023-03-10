from fastapi import FastAPI, Request, HTTPException  
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware 
import motor.motor_asyncio
import pydantic

from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID 
app = FastAPI()

origins=[
    "http://localhost:8000",
    "https://esce3038-lab3-tester.netlify.app"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],  
)
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://orlandobrown:collegeboy@cluster0.qugvaa8.mongodb.net/?retryWrites=true&w=majority")
db = client.water_tank

pydantic.json.ENCODERS_BY_TYPE[ObjectId]= str

@app.get("/profile")
async def get_all_profiles():
    profiles= await db["profile"].find().to_list(1)

    return profiles

@app.post("/profile")
async def create_new_profile(request: Request):
    tank_object = await request.json()



    new_profile = await db["profile"].insert_one(tank_object)
    created_profile = await db["profile"].find_one({"_id": new_profile.inserted_id})

    return created_profile 


@app.get("profile/{data}")
async def get_all_profiles_by_data(data:str):
    profile= await db["profile"].find_one({"_data":
    ObjectId(data)})
    return profile

@app.post("profile/{data}")
async def create_new_profile_by_data(request: Request):
    tank_object= await request.json()

    new_profile= await db["profile"].insert_one(tank_object)
    created_profiles= await db["profile"].find_one({"_id":new_profile.inserted_id})

    return created_profiles

@app.get("/data")
async def retrive_tanks():
    tanks = await db["tank"].find().to_list(999)
    return tanks

@app.delete("/data/{id}", status_code=204)
async def delete_tank(id: str):

    found= await db["tank"].find_one({"_id": ObjectId(id)})
    if (found) is None:
        raise HTTPException(status_code=404, detail="item not found")

    remove_tank= await db["tank"].delete_one({"_id": ObjectId(id)})

    return {"message": "ITEM WAS DELETED"}


@app.patch("/data/{id}")
async def do_update(id: str, request: Request):
    updated= await request.json()
    request= await db["tank"].update_one({"_id":ObjectId(id)}, {'$set': updated})

    if request.modified_count == 1: 
     if(
        updated_tank := await db["tank"].find_one({"_id": id})
       ) is not None:
            return updated_tank



    else:
        raise HTTPException(status_code=404, detail="Item not found")
