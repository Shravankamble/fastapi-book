from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from ..database import get_db

router = APIRouter(
    tags=["Like"]
)

@router.post("/like", status_code=status.HTTP_201_CREATED)
async def like_post(data: schemas.Like, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # if data.like < 0:
    #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Invalid {data.like}")
    like = data.check()
    if like == None:
        raise HTTPException(detail=f"Invalid Like Type {data.like}", status_code=status.HTTP_409_CONFLICT)
    
    post_query = db.query(models.Book).filter(models.Book.user_id == data.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post does not exists")
    
    like_dir = db.query(models.Like).filter(models.Like.posts_id == data.post_id, models.Like.users_id == current_user.user_id)
    liked = like_dir.first()
    
    if data.like == 1:
        if liked:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.name} has already liked the post.")
        like_post = models.Like(posts_id = data.post_id, users_id = current_user.user_id)
        db.add(like_post)
        db.commit()
        return {"message": "Successfully Liked The Post"}
    else:
        if not liked:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like Does Not Exist")
        like_dir.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully Disliked The Post"}