from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app import oauth2

from .. import models, schemas
from ..database import get_db

#region Version 1.0 APIs
router_v10 = APIRouter(
    prefix="/api/v1.0/posts",
    tags=['V1.0_Posts']
)

@router_v10.get("/", response_model=List[schemas.PostOut])  
#@router_v10.get("/")  
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""): 
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()  # if you want to retrive logged in person's posts only
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id) # if you want to print the querry then remove .all() and print it
    # print(posts)'''
    # print(limit)

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 

    # this will limit records to given limit and skip given number of posts
    # this contains does not expect to exactly match the search string. It filters all the titles with search string conatains

    # writing join sql query by default (.join) of sqlalchemy is LEFT INNER JOIN , .label will rename the count column
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
                        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
   
    print(results)
    return results

@router_v10.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) # here new_post is a pydantic model
    # print(current_user.email)
   
    new_post = models.Post(owner_id=current_user.id, **post.dict())  # here instead specifying one by one parameters, **post.dict() will unpack all the data in the post 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve newly created post like we did RETURNING * in sql query
    return new_post

@router_v10.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                       models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")    
    #if post.owner_id != current_user.id: # if want to retrieve owner only posts this has to be checked
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post

@router_v10.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id: # check whether the current user trying to delete his post or not
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router_v10.put("/{id}", response_model=schemas.Post)
def update_post(id: int, pupdated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user: #check whether the current user trying to update his post or not
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(pupdated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
#endregion Version 1.0 APIs

#region Version 1.1 APIs
# router_v11 = APIRouter(
#     prefix="/api/v1.1/posts",
#     tags=['V1.1_Posts']
# )

# @router_v11.get("/", response_model=List[schemas.Post])  
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
#               search: Optional[str] = ""): 
  
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 

#     return posts

#endregion Version 1.1 APIs