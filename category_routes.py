from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from database import engine, Session
from schemas import CategoryModel
from models import User, Category


category_router = APIRouter(
    prefix='/category'
)

session = Session(bind=engine)



@category_router.post("/create")
async def product_page(category: CategoryModel, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == current_user).first()

    if db_user is not None:
        if db_user.is_staff:
            new_category = Category(
                name=category.name
            )
            session.add(new_category)

            session.commit()

            data = {
                "status": status.HTTP_201_CREATED,
                "message": "created category",
                "category_name": new_category.name
            }

            return jsonable_encoder(data)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This page only for Super users")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


