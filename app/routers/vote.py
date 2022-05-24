from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, oauth2
from ..database import get_db

#region Version 2.0 APIs
router_v10 = APIRouter(
    prefix='/api/v1.0/votes',
    tags=['V1.0_Votes']
)

@router_v10.post("/", status_code=status.HTTP_201_CREATED)
def create_votes(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added the vote"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"votes does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted the vote"}


# @router_v10.get("/", response_model=List[schemas.Vote])  
# def get_votes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
#     votes = db.query(models.Vote).filter(models.Vote).all() 
  
#     return votes
#endregion Version 2.0 APIs