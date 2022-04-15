from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from dependency_injector.wiring import inject, Provide

# Application
from app import services
from app.containers import Application
from app.schemas import GenericSchema, AuthSchema


auth_router = APIRouter(prefix="/auth", tags=["Authentication and Authorization"])


@auth_router.post(
    "/login",
    response_model=AuthSchema.LoginResponse,
    responses={
        401: {
            "model": GenericSchema.DetailResponse,
            "description": "Incorrect username or password",
        },
        403: {
            "model": GenericSchema.DetailResponse,
            "description": "Inactive account",
        },
    },
)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authenticate_service: services.AuthenticationService = Depends(
        Provide[Application.services.authentication_service]
    ),
    authorization_service: services.AuthorizationService = Depends(
        Provide[Application.services.authorization_service]
    ),
    user_service: services.UserService = Depends(
        Provide[Application.services.user_service]
    ),
):
    current_user = await authenticate_service.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    logger.debug(f"[Login]::User - {current_user}")

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive account"
        )

    roles = await user_service.get_roles_by_user_id(current_user.id)

    logger.debug(f"[Login]::Roles: {roles}")

    access_token: str = authorization_service.create_jwt_token(
        user_id=current_user.id, scopes=roles
    )

    await user_service.save_user_in_cache(current_user.id)

    return {"access_token": access_token, "token_type": "bearer"}
