from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.params import Body
# from typing import Optional,List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models,schemas,utils
from .database import engine
# from sqlalchemy.orm import Session
# -----------------------------------------------------
from .routers import post,user,auth,vote





models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# try:
#     conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="kteimportasapo",cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection was succesfull!")

# except Exception as error:
#     print("Connecting to database failed")
#     print("Error ",error)
    



# my_posts = [{"title" : "title of post 1","content" : "content of post 1","id" : 1},{"title" : "favorite foods","content" : "I like pizza","id": 2}]

# def find_post(id):
#     for i in my_posts:
#         if i["id"] == id:
#             return i
    
# def find_index_post(id):
#     for i,c in enumerate(my_posts):
#         if c["id"] == id:
#             return i




@app.get("/")
def get_user():
    return {"message": "Hello World"}


# @app.get("/posts")
# def get_posts():
#     cursor.execute("""
#     SELECT *
#     FROM posts;
#     """)
#     posts = cursor.fetchall()
#     print(posts)
#     print("hola mundo")
#     return {"data" : posts}

# SQLALQUEMY-------------------------------------
# @app.get("/sqlalquemy")
# def test_posts(db : Session = Depends(get_db)):

#     # posts = db.query(models.Post).all()
    
#     print("holaaaaaaaaaaaaaaaa")
#     # return posts
#     try:
#         posts = db.query(models.Post).all()
#         return posts
#     except Exception as e:
#         print(f"🔥 Error al obtener posts: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/posts/{id}")
# def get_post(id : int,db : Session = Depends(get_db)):

#     post = db.query(models.Post).filter(models.Post.id_value == id).first()

#     print(post)
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     return {"Valores" : post}


# # SQLAlquemy(get user)------------------------------------------------
# # @app.get("/users/{id}")
# # def get_user(id : int,db : Session = Depends(get_db)):

# #     post = db.query(models.User).filter(models.User.id == id).first()

# #     print(post)
# #     if post == None:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

# #     return post

# # --------------------------------------------------------
# # @app.post("/createposts")
# # def create_posts(payload:dict = Body(...)):
# #     print(payload)
# #     return {"new post" : f'title : {payload["title"]} content : {payload["content"]}'}


# # @app.post("/posts")
# # def create_posts(post : Post):

# #     post_dict = post.dict()
# #     post_dict["id"] = randrange(0,10000000)
# #     my_posts.append(post_dict)


# #     return {"data" : my_posts}
# # SQLALQUEMY-------------------------------------
# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def test_posts(post: schemas.Post,db : Session = Depends(get_db)):

#     # **post.dict()
#     # Creamos el modelo y pasamos los parámetros de la solicitud tipo POST
#     new_post = models.Post(**post.dict())
#     # Agregamos la consulta
#     db.add(new_post)
#     # Ejecutamos la consulta
#     db.commit()
#     # Refrescamos para devolver el valor y que nos aparezca en la solicitud
#     db.refresh(new_post)

#     return {"data" : new_post}



# # SQLALQUEMY(CREATE A USER)-----------------------------------
# # @app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# # def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

# #     hashed_password = utils.hash(user.password)
# #     user.password = hashed_password
# #     new_user = models.User(**user.dict())
# #     db.add(new_user)
# #     db.commit()
# #     db.refresh(new_user)
# #     return new_user
# # --------------------------------------------------------
# # POSTGRESQL----------------------------------------------------------
# # @app.post("/posts",status_code=status.HTTP_201_CREATED)
# # def create_posts(post : schemas.PostCreate):
# #     cursor.execute("""
# #     INSERT INTO posts (title,content,published) VALUES(%s,%s,%s)
    
# #     """,(post.title,post.content,post.published))

# #     conn.commit()

# #     return {"data" : "Succesfully created"}

# # @app.get("/posts/{id}")
# # def get_post(id):
# #     print(id)
# #     return {"post detail" : f"Here is post : {id}"}

# # @app.get("/posts/{id}")
# # def get_post(id : int):
# #     post = find_post(id)
# #     return {"post detail" : post}

# # @app.get("/posts/{id}")
# # def get_post(id : int,response : Response):
# #     post = find_post(id)
# #     if not post:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message" : f"post with id : {id} was not found","error" : response.status_code})
# #         # response.status_code = status.HTTP_404_NOT_FOUND
# #         # return {"message" : f"Post with id : {id} was not found","error" : response.status_code}
# #     return {"post detail" : post}


# # POSTGRESQL---------------------------------------
# # @app.get("/posts/{id}")
# # def get_post(id : int,response : Response):
# #     cursor.execute("""
# #     SELECT * 
# #     FROM posts
# #     WHERE id = %s
# #     """,(str(id)))
# #     data = cursor.fetchall()
# #     print(data)
# #     return {"post detail" : data}

# # @app.delete("/posts/{id}")
# # def delete_post(id: int):
# #     index = find_index_post(id)
# #     my_posts.pop(index)

# #     return {"message" : "Post was succesfully deleted","post" : my_posts}





# # @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# # def delete_post(id: int):
# #     index = find_index_post(id)
# #     if index == None:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")
# #     my_posts.pop(index)
# #     return Response(status_code=status.HTTP_204_NO_CONTENT)
# #     # return {"message" : "Post was succesfully deleted","post" : my_posts}


# # SQLALQUEMY---------------------------------------------------------
# @app.put("/posts/{id}")
# def update_post(id : int, updated_post: schemas.Post, db : Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id_value == id)
#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     post_query.update(updated_post.dict(),synchronize_session=False)
#     db.commit()
#     return {"data" : "Updated succesfully!"}




# # POSTGRESQL---------------------------------------
# # @app.delete("/posts/{id}")
# # def delete_post(id: int):
# #     try:

# #         cursor.execute("""
# #         DELETE
# #         FROM posts
# #         WHERE id = %s
        
        
# #         """,(str(id)))
# #         conn.commit()
# #         return {"Post" : f"Post with id : {id} succesfully deleted"}

# #     except:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")
#     # my_posts.pop(index)
#     # return Response(status_code=status.HTTP_204_NO_CONTENT)



# # SQLALQUEMY----------------------------------------------------
# @app.delete("/posts/{id}")
# def delete_post(id: int, db : Session = Depends(get_db)):

#     post = db.query(models.Post).filter(models.Post.id_value == id)

#     if post.first() == None:

#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     post.delete(synchronize_session=False)

#     db.commit()

#     return {"data" : post.first()}












# --------------------------------------------------


# @app.get("/posts/values/lastest")
# def get_lastest_post():
#     last_post = my_posts[len(my_posts)-1]
#     return last_post


# @app.put("/posts/{id}")
# def update_post(id : int, post: Post):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")
    
#     post_dict = post.dict()
#     post_dict["id"] = id
#     my_posts[index] = post_dict
#     return {"data" : post_dict}

# POSTGRESQL---------------------------------------

# @app.put("/posts/{id}")
# def update_post(id : int, post: Post):
#     cursor.execute("""

#     UPDATE posts
#     SET title = %s,content = %s, published = %s
#     WHERE id = %s
    
#     """,(post.title,post.content,post.published,str(id)))

#     conn.commit()

#     return {"data" : "Updated succesfully!"}


# SQLALQUEMY--------------------------------------
# @app.put("/posts/{id}")
# def update_post(id : int, updated_post: schemas.Post, db : Session = Depends(get_db)):

#     post_query = db.query(models.Post).filter(models.Post.id_value == id)

#     post = post_query.first()

#     if post == None:

#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     post_query.update(updated_post.dict(),synchronize_session=False)

#     db.commit()

#     return {"data" : "Updated succesfully!"}




