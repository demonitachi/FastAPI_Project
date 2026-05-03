from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import List, Set, Optional
from uuid import UUID
from datetime import datetime

app = FastAPI()

# 1. Lowercase 'class'
# 2. Updated Config for Pydantic V2
class Person(BaseModel):
    id: UUID
    name: str = Field(..., min_length=1, max_length=100, title="Name", description="1-100 chars")
    age: int = Field(..., gt=0, lt=150)
    # Use 'pattern' instead of 'regex' for Pydantic V2
    email: str = Field(..., pattern=r'^\S+@\S+\.\S+$')
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    favorite_colors: List[str] = []
    tags: Set[str] = set()

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "age": 30,
                "email": "johndoe@gmail.com",
                "is_active": True,
                "created_at": "2024-06-01T12:00:00Z",
                "favorite_colors": ["red", "blue"],
                "tags": ["developer"]
            }
        }
    }

class Login(BaseModel):
    username: str
    password: str

class ImageModel(BaseModel):
    url: HttpUrl
    persons: List[Person]

# Corrected Login: If you want Form data, use Form() in params.
# If you want JSON, just use the Login model.
@app.post('/login')
def login_user(username: str = Form(...), password: str = Form(...)):
    return {"message": f"User {username} logged in successfully!"}

@app.post('/image/{uuid}')
def upload_image(uuid: UUID, image: ImageModel, no_of_persons: int = 1):
     return {
         "message": f"Image {uuid} uploaded!",
         "data": image,
         "count": no_of_persons
     }

@app.get('/')
def hello():
    return {"message": "Hello World"}

@app.get('/property/{id}')
def get_property(id: int = 1, comment_id: int = 10, qid: Optional[int] = None):
    return {
        "id": id,
        "comment_id": comment_id,
        "qid": qid
    }

@app.get('/movies')
def movies():
    return {"movies": ["The Dark Knight", "Pulp Fiction"]}