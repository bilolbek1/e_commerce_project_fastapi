from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from database import Session, engine
from models import User
from schemas import SignUpModel, LoginModel, ProfileModel
from fastapi.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash
import datetime


auth_router = APIRouter(
    prefix="/auth"
)

session = Session(bind=engine)


@auth_router.get("/")
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")
    return {"message": "Hello SignUp Page"}




@auth_router.post("/signup")
async def signup(user: SignUpModel):
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the username already exists")

    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the email already exists")


    new_user = User(
        username= user.username,
        email= user.email,
        first_name= user.first_name,
        last_name= user.last_name,
        password= generate_password_hash(user.password),
        is_staff= user.is_staff,
        is_active= user.is_active
    )

    session.add(new_user)
    session.commit()

    data = {
        "id":new_user.id,
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "password": new_user.password,
        "is_active": new_user.is_active,
        "is_staff": new_user.is_staff
    }

    return jsonable_encoder(data)



@auth_router.post("/login")
async def login(user:LoginModel, Authorize:AuthJWT=Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_limit_time = datetime.timedelta(minutes=60)
        refresh_limit_time = datetime.timedelta(days=5)

        access_token = Authorize.create_access_token(subject=db_user.username,
                                                     expires_time=access_limit_time)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username,
                                                       expires_time=refresh_limit_time)

        token = {
            "access": access_token,
            "refresh": refresh_token
        }

        data = {
            "success": True,
            "status": 200,
            "message": "Succusfully logged in",
            "token": token
        }


        return jsonable_encoder(data)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid username or password")





@auth_router.get('/login/refresh')
async def refresh_access(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        user = session.query(User).filter(User.username == current_user).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        access_limit_time = datetime.timedelta(minutes=60)

        new_access = Authorize.create_access_token(subject=user.username,
                                                   expires_time=access_limit_time)

        response = {
            "success": True,
            "status": 200,
            "message": "Get new access token",
            "token": new_access
        }

        return jsonable_encoder(response)


    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail="Invalid refresh token")




@auth_router.get("/user/profile")
async def profile(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    currnet_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == currnet_user).first()

    user_data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_active": user.is_active
    }

    return jsonable_encoder(user_data)


#
#
# @auth_router.patch("/user/profile/update")
# async def profile_update(profile_data: ProfileModel, Authorize: AuthJWT=Depends()):
#     try:
#         Authorize.jwt_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Invalid token")
#
#     current_user = Authorize.get_jwt_subject()
#     user = session.query(User).filter(User.username == current_user).first()
#
#     if user == profile_data:
#
#         user.username = profile_data.username
#         user.first_name = profile_data.first_name
#         user.last_name = profile_data.last_name
#         user.email = profile_data.email
#         user.is_active = profile_data.is_active
#
#         session.commit()
#
#         user_profile = {
#             "id": user.id,
#             "username": profile_data.username,
#             "first_name": profile_data.first_name,
#             "last_name": profile_data.last_name,
#             "email": profile_data.email,
#             "is_active": profile_data.is_active
#         }
#
#         data = {
#             "success": True,
#             "status": status.HTTP_200_OK,
#             "message": "Successfully updated your profile",
#             "user": user_profile
#         }
#
#         return jsonable_encoder(data)
#
#
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                         detail="Po'q xato bo'ldi")
#
#













