from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from database import engine, Session
from models import User, Product
from schemas import ProductModel, CategoryModel


product_router = APIRouter(
    prefix='/product'
)


session = Session(bind=engine)



@product_router.get("/")
async def product_page(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    return {"message": "This is product page"}



@product_router.post("/create_product")
async def create_product(product:ProductModel, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()

    db_user = session.query(User).filter(User.username == current_user).first()

    if db_user is not None:
        if db_user.is_staff:
            new_product = Product(
                name=product.name,
                description=product.description,
                old_price=product.old_price,
                new_price=product.new_price
            )

            new_product.user = db_user
            new_product.category_id = product.category_id

            session.add(new_product)
            session.commit()


            product_data = {
                "id": new_product.id,
                "user_id": new_product.user_id,
                "name": new_product.name,
                "description": new_product.description,
                "old_price": new_product.old_price,
                "new_price": new_product.new_price,
                "category_id": new_product.category_id
            }

            data = {
                "success": True,
                "status": status.HTTP_201_CREATED,
                "message": "Successfully product created",
                "product_data":product_data
            }

            return jsonable_encoder(data)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This page only for Super users")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")




@product_router.get("/list")
async def products_list(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    products = session.query(Product).all()

    product_list = [
        {
            "id": i.id,
            "user_id": i.user_id,
            "name": i.name,
            "description": i.description,
            "old_price": i.old_price,
            "new_price": i.new_price,
            "category_id": i.category_id
        }
        for i in products
    ]

    return jsonable_encoder(product_list)




@product_router.get("/{id}")
async def products_list(id: int, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    product = session.query(Product).filter(Product.id == id).first()

    if product is not None:
        return jsonable_encoder(product)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Product not found with this id")




@product_router.delete("/{id}/delete")
async def delete(id: int, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user is not None:
        if user.is_staff:
            product = session.query(Product).filter(Product.id == id).first()

            if product is not None:
                session.delete(product)
                session.commit()

                data = {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": "Successfully deleted product",
                    "product_id": product.id
                }

                return jsonable_encoder(data)

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product not found with this id")


        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This page only for Super users")


    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")





@product_router.put("/{id}/update")
async def product_update(id: int, product: ProductModel, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        update_product = session.query(Product).filter(Product.id == id).first()

        update_product.name = product.name
        update_product.description = product.description
        update_product.old_price = product.old_price
        update_product.new_price = product.new_price

        session.commit()

        updated_product = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "old_price": product.old_price,
            "new_price": product.new_price
        }

        data = {
            "success": True,
            "status": 201,
            "message": "Successfully updated product",
            "product":updated_product

        }

        return jsonable_encoder(data)


    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="This page only for Super users")























































