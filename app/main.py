# from multiprocessing import synchronize
# from turtle import title

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from . import models  # . represents the current directory
from .database import engine
from .routers import user, auth, post, vote
#from .routers.v10 import post as post_v10
from .config import settings



# models.Base.metadata.create_all(bind=engine) # when alembic is used to DB migration then this is no longer needed.
# But can keep if you want to create all the table at the first place

app = FastAPI() # create an instance of FastAP

'''
middleware is a function running just before every request. 
'''
# origins = ["https://www.google.com"]  # if need to allow all the domains to access then user ["*"]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # it is possible to restrict post methods if needed
    allow_headers=["*"],
)

# set routers to wire up each module api routers
app.include_router(post.router_v10)
#app.include_router(post.router_v11)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router_v10)

#region Old stuff 
# this is no need when you use SqlAlchemy ORM

# set DB connection and do this in a while loop until connect to the DB otherwise no point of doing the rest of application if unable to connect to the DB

# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='$un$hin3',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull!')
#         break
#     except Exception as error:
#         print('Connecting to databae failed')
#         print(f'Error: {error}')
#         time.sleep(2)

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#    for i, p in enumerate(my_posts):
#       if p["id"] == id:
#           return i

#endregion Old stuff

#region API methods
# path operation or route
@app.get("/")  # this decorator convert the normal method to a fast api method and within braket it specifies the path url to access (no longer need this)
def root(): #async def root(): async optional and the name root can be any (login, login_user, etc.)
    return {"message": "Welcome to Fast API!"}

#region API methods using sql commands 

# @app.get("/posts")  
# def get_posts(): 
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data": posts}

# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
#     post = cursor.fetchone()
#     # post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id: {id} was not found"}
#     return {f"post_detail": post}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post): # here new_post is a pydantic model
#     # post_dict = post.dict()
#     # post_dict['id'] = randrange(0, 1000000)
#     # my_posts.append(post.dict())
#     '''
#     cursor.execute(f" INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")

#     Even though above works fine we should not do this since this is vulnarable to sql injection attacks.
#     '''
#     cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title,
#     post.content, post.published))
#     new_post = cursor.fetchone()  # upto here the sql query staged data

#     conn.commit() # need to commit staged data to go to the DB
#     return {"data": new_post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
#     deleted_post = cursor.fetchone()
    
#     conn.commit()
#     # index = find_index_post(id)

#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     # my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def update_post(id: int, post: Post):
#     cursor.execute(""" UPDATE posts SET title = %s, content =%s, published = %s WHERE id = %s RETURNING * """, (post.title, 
#                     post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
    
#     #index = find_index_post(id)

#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     # post_dict = post.dict()
#     # post_dict['id'] = id
#     # my_posts[index] = post_dict
#     return {"data" : updated_post}

#endregion API methods using sql commands 

#region API methods using Sqlalchemy ORM 

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

#endregion API methods using Sqlalchemy ORM 

#endregion API methods