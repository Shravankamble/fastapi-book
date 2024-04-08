# from typing import Optional
# from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel
# import random

# app = FastAPI()

# @app.get("/secret")
# async def secret():
#     return {"CONFIDENTIAL": "I am going to become a billionaire!"}

# class Verifier(BaseModel):
#     id: int = random.randint(1, 10000)
#     Email: str = "Invalid"
#     password: str = "Invalid"

# account_list = [{"id": 1,"Email": "shravankamble014@gmail.com", "password": "sbk@10"}, 
# {"id": 2,"Email": "Anonymous@gmail.com", "password": "Knowwhat"}]

# @app.get("/github")
# def alllogs():
#     return {"Data": account_list}

# @app.post("/github/Login", status_code=status.HTTP_201_CREATED)
# def LoginIn(Login: Verifier):
#     data = Login.dict()
#     account_list.append(data)
#     return {"details": "New User Logged In!"}


# def find_email(psw, resp: Response):
#     for i in account_list:
#         if i["password"] != psw:
#             continue
#         else:
#             return i
#     resp.status_code = status.HTTP_404_NOT_FOUND
#     return {"details": "Password Not Found!"}

# def github_email_update(id):
#     for i, j in enumerate(account_list):
#         if j["id"] == id:
#             return i

# def github_delete_acc(id):
#     for i, p in enumerate(account_list):
#         if p["id"] == id:
#             return i

# def find_id(id):
#     for i in my_books:
#         if i["id"] != id:
#             continue
#         else:
#             return i
#     return {"details": "ID doesn't exists!"}

# def delete_posts_id(id):
#     for i, p in enumerate(my_books):
#         if p['id'] == id:
#             return i

# @app.get("/github/Login/{password}")
# def github(password, resp: Response):
#     data = find_email(str(password), resp) 
#     return {"Data": data}

# @app.put("/github/Login/{id}", status_code=status.HTTP_201_CREATED)
# async def git_update_email(id: int, gitacc: Verifier):
#     index = github_email_update(id)
#     if not id:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"given Email: {id} Not Found!")
#     new_email = gitacc.dict()
#     new_email['id'] = id
#     account_list[index] = new_email
#     return {"update": f"New {new_email} updated"}

# @app.delete("/github/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_gitacc(id: int):
#     get_id = github_delete_acc(int(id))
#     account_list.pop(get_id)
#     return {"details": "Account Deleted!"}

""" Postgresql """
# while True:
#     try:
#         # connecting to database using psycopg2 module
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='shravankamble', cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("succesfully connected to the database!")
#         break
#     except Exception as error:
#         print("unable to connect to server!")
#         print("error is : ", error)
#         time.sleep(2)

# class Tables(BaseModel):
#     n: int = random.randint(1, 100)

# @app.post("/customtable")
# async def custom(number: Tables):
#     n = number.n
#     list = []

#     count = 1

#     while (count <= 11):
#         list.append(n * count)
#         count += 1

#         if (count == 11):
#             break

#     stringlist = ' '.join(map(str, list))
#     return f"Table Of An random Integer :  {stringlist}"

# @app.get("/table")
# async def custom():
#     n = random.randint(1, 100)
#     list = []

#     shravan = 1

#     while (shravan <= 11):
#         list.append(n * shravan)
#         shravan += 1

#         if (shravan == 11):
#             break

#     stringlist = ' '.join(map(str, list))
#     return f"Table Of An random Integer :  {stringlist}"

""" Old unused Learning endpoints """

# @router.put("/posts/publishedBooks/{user_id}", status_code=status.HTTP_200_OK)
# async def published_books(user_id: int, published: schemas.PublishedBook, db: Session = Depends(get_db)):
#     get_publish_book = db.query(models.Book).filter(models.Book.user_id == user_id)
#     update_published = get_publish_book.first()

#     if not update_published:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {user_id} doesn't exists")

#     get_publish_book.update(published.dict(), synchronize_session=False)
#     db.commit()
#     return get_publish_book.first()

# @router.put("/sales/{user_id}")
# async def Update_Sales(user_id: int, sales: schemas.UpdateSales, db: Session = Depends(get_db)):
#     Found_user_id = db.query(models.Book).filter(models.Book.user_id == user_id)
#     update_sale = Found_user_id.first()

#     if not update_sale:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {user_id} doesn't found")

#     Found_user_id.update(sales.dict(), synchronize_session=False)
#     db.commit()
#     return Found_user_id.first()

# @router.get("/publishedBooks")
# async def published(db: Session = Depends(get_db)):
#     published_book = db.query(models.Book).filter(models.Book.published == 'true')
#     get_all = published_book.all()
#     return get_all