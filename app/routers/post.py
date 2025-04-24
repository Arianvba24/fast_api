from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2,database
from sqlalchemy.orm import Session
from ..database import engine,get_db
from typing import Optional,List
from sqlalchemy import func


router = APIRouter(

    prefix="/posts",
    tags=["Posts"]
)



# @router.get("/")
# def test_posts(db : Session = Depends(get_db)):
    

#     try:
#         posts = db.query(models.Post).all()
#         return posts
#     except Exception as e:
#         print(f"🔥 Error al obtener posts: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/{id}")
# def get_post(id : int,db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

#     post = db.query(models.Post).filter(models.Post.id_value == id).first()
    

#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perfom requested action")

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     return {"Valores" : post}

# SQLALQUEMY(INNERJOIN)----------------------------------------------
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int,db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post,func.count(models.Votes.post_id).label("votes"),models.Post.owner_id).join(models.Votes,models.Votes.post_id == models.Post.id_value,isouter=True).group_by(models.Post.id_value).filter(models.Post.id_value == id).first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perfom requested action")

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

    return post




# SQLALQUEMY(FOREIGN KEYS)-----------------------------------
# @router.get("/{id}")
# def get_post(id : int,db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

#     post = db.query(models.Post).filter(models.Post.id_value == current_user.id).all()

#     # print(post)
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     return post


# @router.get("/",response_model=List[schemas.Post])
# def test_posts(db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int = 10,skip: int = 1,search: Optional[str] = ""):
    
#     try:
#         print(search)
#         posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
#         # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#         return posts
#     except Exception as e:
#         print(f"🔥 Error al obtener posts: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# SQLALQUEMY(INNERJOIN)----------------------------------------------
# @router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def test_posts(db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int = 10,skip: int = 1,search: Optional[str] = ""):
    
    try:
    
        posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

        results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id_value,isouter=True).group_by(models.Post.id_value).all()
        print(results)
        # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        return results
    except Exception as e:
        print(f"🔥 Error al obtener posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# SQLAlquemy(get user)------------------------------------------------
# @app.get("/users/{id}")
# def get_user(id : int,db : Session = Depends(get_db)):

#     post = db.query(models.User).filter(models.User.id == id).first()

#     print(post)
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     return post

# --------------------------------------------------------
# @app.post("/createposts")
# def create_posts(payload:dict = Body(...)):
#     print(payload)
#     return {"new post" : f'title : {payload["title"]} content : {payload["content"]}'}


# @app.post("/posts")
# def create_posts(post : Post):

#     post_dict = post.dict()
#     post_dict["id"] = randrange(0,10000000)
#     my_posts.append(post_dict)


#     return {"data" : my_posts}
# SQLALQUEMY-------------------------------------
# @router.post("/",status_code=status.HTTP_201_CREATED)
# def test_posts(post: schemas.Post,db : Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):

#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return {"data" : new_post}

# @router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def test_posts(post: schemas.Post,db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

#     print(current_user.email)
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post

# SQLALQUEMY(FOREIGN KEYS)-----------------------------------
@router.post("/",status_code=status.HTTP_201_CREATED)
def test_posts(post: schemas.PostCreate,db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # print(current_user.email)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# SQLALQUEMY(CREATE A USER)-----------------------------------
# @app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
# --------------------------------------------------------
# POSTGRESQL----------------------------------------------------------
# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post : schemas.PostCreate):
#     cursor.execute("""
#     INSERT INTO posts (title,content,published) VALUES(%s,%s,%s)
    
#     """,(post.title,post.content,post.published))

#     conn.commit()

#     return {"data" : "Succesfully created"}

# @app.get("/posts/{id}")
# def get_post(id):
#     print(id)
#     return {"post detail" : f"Here is post : {id}"}

# @app.get("/posts/{id}")
# def get_post(id : int):
#     post = find_post(id)
#     return {"post detail" : post}

# @app.get("/posts/{id}")
# def get_post(id : int,response : Response):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message" : f"post with id : {id} was not found","error" : response.status_code})
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message" : f"Post with id : {id} was not found","error" : response.status_code}
#     return {"post detail" : post}


# POSTGRESQL---------------------------------------
# @app.get("/posts/{id}")
# def get_post(id : int,response : Response):
#     cursor.execute("""
#     SELECT * 
#     FROM posts
#     WHERE id = %s
#     """,(str(id)))
#     data = cursor.fetchall()
#     print(data)
#     return {"post detail" : data}

# @app.delete("/posts/{id}")
# def delete_post(id: int):
#     index = find_index_post(id)
#     my_posts.pop(index)

#     return {"message" : "Post was succesfully deleted","post" : my_posts}





# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#     # return {"message" : "Post was succesfully deleted","post" : my_posts}


# SQLALQUEMY---------------------------------------------------------
# @router.put("/{id}")
# def update_post(id : int, updated_post: schemas.Post, db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
#     post_query = db.query(models.Post).filter(models.Post.id_value == id)
#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     post_query.update(updated_post.dict(),synchronize_session=False)
#     db.commit()
#     return {"data" : "Updated succesfully!"}


# SQLALQUEMY(FOREIGN KEY)----------------------------------------------------
@router.put("/{id}")
def update_post(id : int, updated_post: schemas.PostCreate, db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id_value == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perfom requested action")


    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data" : f"Updated succesfully post {id}!"}

# POSTGRESQL---------------------------------------
# @app.delete("/posts/{id}")
# def delete_post(id: int):
#     try:

#         cursor.execute("""
#         DELETE
#         FROM posts
#         WHERE id = %s
        
        
#         """,(str(id)))
#         conn.commit()
#         return {"Post" : f"Post with id : {id} succesfully deleted"}

#     except:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)



# SQLALQUEMY----------------------------------------------------
# @router.delete("/{id}")
# def delete_post(id: int, db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

#     post = db.query(models.Post).filter(models.Post.id_value == id)

#     if post.first() == None:

#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

#     post.delete(synchronize_session=False)

#     db.commit()

#     return {"data" : post.first()}

# SQLALQUEMY(FOREIGN KEY)----------------------------------------------------

@router.delete("/{id}")
def delete_post(id: int, db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id_value == id)

    post = post_query.first()

    # print(current_user.id,post.owner_id)
    if post == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perfom requested action")

    post_query.delete(synchronize_session=False)

    db.commit()

    return {"detail" : f"Successfuly deleted post {id}"} 