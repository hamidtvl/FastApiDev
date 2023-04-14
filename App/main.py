from typing import List, Optional
from fastapi import FastAPI ,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
#import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas,utils,oauth2
from .database import engine,get_db
from sqlalchemy.orm import Session
from .Router import post,user,auth,vote
from .Config import setting
from fastapi.middleware.cors import CORSMiddleware
print(setting.database_hostname)

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)




# try:
#     conn = psycopg2.connect(host = 'localhost',port=5433,database ='fastapi',user = 'postgres',password= 'H@mid77',cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('database connection succsessfull!')
# except Exception as error:
#     print('connecting to database failed')
#     print('error:',error)

# my_posts = [{'title':'title of the post','content':'content of the post','id':1},
#            {'title':'favorite foods','content':'i like pizza','id':2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id']== id:
#             return p
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
async def root():
    return {"message":"welcome to my api."}
