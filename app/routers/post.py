from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(# + "/id" = /posts/{id}

    prefix="/posts", 

    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut]) #get is used for retrieving data

def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 20, skip: int = 0, search: Optional[str] = ''):

    '''

    cursor.execute("SELECT * FROM posts")

    posts = cursor.fetchall()

    '''

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #select posts.*, count(votes.post_id) from posts left outer join votes on posts.id = votes.post_id where = ? group by posts.id limit = ? offset = ?

    return posts 


@router.get("/own", response_model=List[schemas.PostOut])

def get_own_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()
    if not posts:
        raise HTTPException(status_code=404, detail=f"No posts created")
    return posts 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)

def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 

    #user_id depends - ensures that a user must be logged in to create a post


    '''

    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()

    '''


    new_post = models.Post(owner_id = current_user.id, **post.dict())

    db.add(new_post)

    db.commit()

    db.refresh(new_post) #equivalent of RETURNING in sql

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)

def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #to deal with errors if input is not string

    # cursor.execute("SELECT * FROM posts WHERE id = %s", str(id))

    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:

        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")

        # response.status_code = 404 #if no post, return 404 status code: not found
        # OR
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"Post with id {id} was not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)


    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", str(id))

    # deleted = cursor.fetchone()

    # conn.commit()

    if post.first() == None:

        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")

    if post.first().owner_id != current_user.id:

        return Response(status_code=status.HTTP_403_FORBIDDEN)


    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)

def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))

    # updated = cursor.fetchone()

    # conn.commit()

    if post_query.first() == None:

        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")

    if post.first().owner_id != current_user.id:

        return Response(status_code=status.HTTP_403_FORBIDDEN)

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    

    return post_query.first()