from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Text,Optional,Union
from datetime import datetime
from uuid import uuid4 as uuid
from fastapi.middleware.cors import CORSMiddleware

#Inicializamos FastAPI
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Creamos arreglo de Posts
posts = []

#Modelo de los Post
class Post(BaseModel):
        id:Optional[str | None ] = None
        title:str
        author:str
        content:Text
        created_at: datetime = datetime.now()
        published_at:datetime | None = None
        published: bool = False

# Creamos Rutas

#creamos la ruta principal
@app.get('/')
def read_root():
        return{"Welcome" : "Welcome to my API"}


@app.get('/posts')
def get_post():
        return posts

@app.post('/posts')
def save_post(post:Post):
        post.id = str(uuid())
        posts.append(post.model_dump())
        return "recibido"

@app.get('/posts/{post_id}')
def get_Post(post_id:str):
      for post in posts:
        if post["id"] == post_id:
               return post
        raise HTTPException(status_code=404,detail="Post not found" )


@app.delete('/posts/{post_id}')
def delete_Post(post_id:str):
      for index,post in enumerate(posts):
        if post["id"] == post_id:
               posts.pop(index)
               return "El post ha sido eliminado"
        raise HTTPException(status_code=404,detail="Post not found" )
      
@app.put('/post/{post_id}')
def update_post(post_id:str,updatedPost:Post):
      for index,post in enumerate(posts):
             if post["id"] == post_id:
                   posts[index]["title"]= updatedPost.title
                   posts[index]["content"]= updatedPost.content
                   posts[index]["author"]= updatedPost.author
                   return "El Post ha sido correctamente Actualizado"
             raise HTTPException(status_code=404,detail="Post not found" )
       
            