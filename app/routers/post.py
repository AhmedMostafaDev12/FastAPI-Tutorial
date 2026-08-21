from typing import Optional, List 
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from .. import models,schemas, Oauth2
from ..database import get_db, engine
from sqlalchemy.orm import Session
from sqlalchemy import func


models.Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



# / means the root path of the application. When a GET request is made to the root URL ("/"), the read_root function will be executed, returning a JSON response with the message {"Hello": "World"}.
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return [{"post": post, "vote": vote} for post, vote in results]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    #    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                   (post.title, post.content, post.published))
    #    new_post = cursor.fetchone()
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"latest_post": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(Oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    post, vote = result
    return {"post": post, "vote": vote}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user: models.User = Depends(Oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()
    
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"post with id: {id} was successfully deleted"}

@router.put("/{id}",response_model=schemas.Post)
# you recieve the data from the body of the request and you recieve the id from the path parameter
# the data stored in post is of type Post, which is a Pydantic model that defines the expected structure of the request body. The id parameter is of type int, which is extracted from the path parameter in the URL.
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(Oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # post_query  ──.first()──►  SELECT   (read,  no commit needed)
    #  │
    #  └──────.update()──►  UPDATE   (write, needs db.commit())

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()