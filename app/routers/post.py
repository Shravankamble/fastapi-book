from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, sessionLocal, get_db
from typing import List, Optional

router = APIRouter(
    # prefix="/posts",
    tags=['Posts']
)

""" parameter limit in function root could be defined by the user as a query parameter in the URL, 
    But if the user doesn't provide the quey parameter it'll be set as whatever integer is passed in function as default"""    
@router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.GetPost])
@cache(expire=30)
async def root(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), limit: int = 10):
    # This query run using psycopg2 module where you have to pass raw sql
    #                           ↓
    # cur.execute(""" SELECT * FROM books """)
    # books = cur.fetchall()

    # This query is run using python sqlalchemy, but in code itself its running sql
    #                        ↓
    books = db.query(models.Book).limit(limit).all()
    return books

@router.get("/posts", response_model=List[schemas.GetPost])
async def search_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = " ", limit: int = 0):
    find_post = db.query(models.Book).filter(models.Book.book_name.contains(search)).limit(limit).all()
    return find_post

"""this route is to get all posts from an particular user"""
@router.get("/getposts", status_code=status.HTTP_200_OK, response_model=List[schemas.GetPost])
async def get_specific_users_posts(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), limit: int = 10):
    specific_user_posts = db.query(models.Book).filter(models.Book.username == current_user.name).all()
    
    if not specific_user_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {current_user.name} doesn't have any posts yet")
    
    return specific_user_posts

# addes a new book and commits it in the database! 
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.CreatePostResp)
async def new_posts(new_book: schemas.CreatePost, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # cur.execute(""" INSERT INTO books (title, author, published) VALUES (%s, %s, %s) RETURNING * """ (create.title, create.author, create.published))
    # new_post_book = cur.fetchone()
    # conn.commit()
    # print(current_user.email)
    new_post = models.Book(username=current_user.name, **new_book.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/{user_id}", status_code=status.HTTP_200_OK)
async def get_password(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # here is how you find a post using raw sql in psycopg2 module
    #                            ↓
    # cur.execute(""" SELECT * FROM books WHERE id = %s """, (str(id),))
    # id_info = cur.fetchone()
    # <------------------------------!------------------------------------>
    # and here's how you find a post/book using sqlalchemy where you dont have to use raw sql.
    post_to_find = db.query(models.Book).filter(models.Book.user_id == user_id).first()

    if not post_to_find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The given id: {user_id} doesn't exists")

    return {"data": post_to_find}

@router.delete("/posts/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT) 
async def delete_post(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # cur.execute(""" DELETE FROM books WHERE id = %s RETURNING * """, (str(id),))
    # deleted_id = cur.fetchone()
    
    delete_user_id = db.query(models.Book).filter(models.Book.user_id == user_id)
    delete_post = delete_user_id.first()

    if delete_user_id.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The given id: {user_id} doesn't exists")
    
    if delete_post.username != current_user.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{current_user.name} your Not authorized to perform this task! ")

    delete_user_id.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/update/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.CreatePostResp)
async def update_info(user_id: int, update_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # if your gonna use psycopg2 module read this.
    # cur.execute() function executes the query 
    #     cur.execute(""" UPDATE books SET title = %s, author = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.author, post.published, (str(id),)))
    #     cur.fetchone() function fetches(gathers or collects) all data from the above query 
    #     updated_book = cur.fetchone()
    #     if updated_book == None:
    #         # if The id your looking for does not exists its gonna raise this httpexception
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID doesn't exists!")
    # conn.commit() function is used to commit all the data into real database which is fastapi, on line 130
    # if you didn't use conn.commit() function its just gonna add it to the book its never gonna add it to the database
    # so whenever you run a query and wanna add it to database use conn.commit() function 
    #         conn.commit()
    find_post_to_update = db.query(models.Book).filter(models.Book.user_id == user_id)
    update_posts = find_post_to_update.first()

    if update_posts.username != current_user.name:
        raise HTTPException(detail=f"{current_user.name} your Not authorized to perform this task! ", status_code=status.HTTP_403_FORBIDDEN)

    if not update_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {user_id} doesn't exists")

    find_post_to_update.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return find_post_to_update.first()

@router.get("/get/routes")
async def get_all_post_route(routes: schemas.GetAllRoutes, status_code=status.HTTP_200_OK):
    all_routes = routes
    return {"routes": all_routes}

@router.get("/published", status_code=status.HTTP_200_OK)
async def get_all_published_books(db: Session = Depends(get_db), limit: int = 2, current_user: int = Depends(oauth2.get_current_user)):
    is_published = db.query(models.Book).filter(models.Book.published == 'true').all()
    return {"published": is_published}

@router.post("/search/user")
async def find_user(user: schemas.FindUser, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    find_search_user = db.query(models.Book).filter(models.Book.username == user.name).all()
    
    if not find_search_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user.name} doesn't exist")
    
    return find_search_user

@router.patch("/patch/{user_id}")
async def patchAny(user_id: int, data: dict, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.Book).filter(models.Book.user_id == user_id)
    user_first = user.first()
    if user_first.username != current_user.name:
        raise HTTPException(detail=f"{current_user.name} your Not authorized to perform this task!", status_code=status.HTTP_403_FORBIDDEN)
    user.update(data)
    db.commit()
    return user.first()