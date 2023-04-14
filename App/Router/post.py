from fastapi import FastAPI ,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix='/posts',
                   tags= ['Posts'])



@router.get('/',response_model=List[schemas.PostOut])
def get_posts(db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user),
              limit:int = 10,skip :int = 0, search: Optional[str] =""):
    # cursor.execute("""select * from posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()

    results  = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    

    return results
    

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" insert into posts (title,content,published) values(%s,%s,%s)  returning *""" , (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}',response_model=schemas.PostOut)
def get_post(id:int,response: Response,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    # post = find_post(id)
    post = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} was not found')
        # response.status_code =status.HTTP_404_NOT_FOUND
        # return {"message":f'post with id {id} was not found'}
    # cursor.execute("""select * from posts where id = %s """, (str(id)))
    # test_post = cursor.fetchone()
    return post

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" delete from posts where id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post = db.query(models.Post).filter(models.Post.id ==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} doesnt exist')
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='you cannot access this post')
    post.delete(synchronize_session = False)
    db.commit()
    return {'here is the deleted post': post}



@router.put('/{id}')
def updated_post(id:int,post:schemas.PostCreate,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" update posts set title = %s , content = %s , published =%s where id = %s returning *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone() 
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} doesnt exist')
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='you cannot access this post')
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()