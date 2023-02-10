from fastapi import FastAPI, Request
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
import pydantic

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
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://orlandobrown:<password>@cluster0.qugvaa8.mongodb.net/?retryWrites=true&w=majority")
db = client.water_tank

pydantic.json.ENCODERS_BY_TYPE[ObjectId]= str

@app.get("/profile")
async def get_all_profiles():
    profiles= await
    db["profile"].find().to_list(999)

    return profiles

@app.post("/profile")
async def create_new_profile(request: Request):
    tank_object = await request.json()



    new_profile = await db["profile"].insert_one(todo_object)
    created_profile = await db["profile"].find_one({"last_updated": new_profile.insert_last_updated})

    return created_profile 


    @app.get("profile/{data}")
    async def get_all_profiles_by_data(data:str):
        profile= await
        db["profile"].find_one({"_data":
        ObjectId(data)})
        return profile

@app.post("profile/{data}")
async def create_new_profile_by_data(request: Request):
    tank_object= await request.json()

    new_profile= await
    db["profile"].insert_one(tank_objects)
    created_profiles= await
    db["profile"].find_one({"last_updated":new_profiles.insert_last_updated})

    return created_profiles

@app.get("/data")
async def retrive_tanks():
    tanks = await db["tank"].find().to_list(999)
    return tanks
