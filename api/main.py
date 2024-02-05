# Copyright 2024 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import bcrypt

from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session

import uuid
from typing import Generator

import models
import schema

from db import engine
from models import Base


Base.metadata.create_all(engine)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session

app = FastAPI()

session_token = ""

secret_key = "blablabla"


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/register")
def register_user(user: schema.UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = bcrypt.hashpw(user.password.encode('utf-8'), secret_key)

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}

@app.get("/signin")
def signin(user: schema.User, session = Depends(get_session)):
    global session_token 
    
    enc_password = bcrypt.hashpw(user.password.encode('utf-8'), secret_key)
    user = session.query(models.User).filter_by(email=user.email, password=enc_password)
    token =  uuid.uuid4()
    if user.first() is None:
        return {"message": "Username or password is incorrect."}
    
    session_token = token
    
    return {"message": "Successfully signed in."}

    
@app.get("/signout")
def signout(token: str, session = Depends(get_session)):
    
    if token != session_token: 
        return {"message": "No user to sign out."}
    
    if token == session_token: 
        session_token = ""
    
    return {"message": "User signed out successfully."}
