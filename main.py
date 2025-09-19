from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Employee model
 
class Employee_model (BaseModel):
    Employee_id: int
    Employee_name: str
    Employee_age: int
    Employee_department: str

# path operation =path + http method + function
@app.get("/users")
async def list_users():
    return [{"name":"Kirankumar", "designation":"ASE", "qualification":"MCA"},
            {"name":"xyz", "designation":"ase", "qualification":"btecg"}
            ]

@app.post("/users")
async def create_user(user:User):
    return {"Message":"User created successfully", "user": User}

@app.delete("/users/{user_name}")
async def delete_user(user_name:str):
    return {"Message": f"User {user_name} deleted"}

@app.put("/users/user_id")
async def update_user(user_id: int, user:user):
    return {"message": f"user {user_id} updated successfully"}