from fastapi import APIRouter , Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas,models,utils,oauth2

router = APIRouter(tags=['authentication'],prefix='/login')

@router.post('/',response_model=schemas.token)
def login(user_credential : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials')
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid credentials')
    
    #create token
    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {'access_token': access_token , "token_type": "bearer"}

