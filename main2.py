from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# MongoDB connection URI
MONGO_URI = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URI)
db = client["test_db"]      # or your actual database name
collection = db["users"]

client = AsyncIOMotorClient(MONGO_URI)

# Select database and collection
db = client["test_db"]
collection = db["users"]

# Pydantic model for request body
class User(BaseModel):
    name: str
    email: str

# Helper function to convert MongoDB document
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }

@app.post("/users/")
async def create_user(user: User):
    result = await collection.insert_one(user.dict())
    new_user = await collection.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/")
async def list_users():
    users = []
    async for user in collection.find():
        users.append(user_helper(user))
    return users

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    result = await collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user.dict()}
    )
    if result.modified_count == 1:
        updated_user = await collection.find_one({"_id": ObjectId(user_id)})
        return user_helper(updated_user)
    existing_user = await collection.find_one({"_id": ObjectId(user_id)})
    if existing_user:
        return user_helper(existing_user)  # nothing changed, but return current
    raise HTTPException(status_code=404, detail="User not found")