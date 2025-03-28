from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta
from jose import jwt, JWTError

from app.database import async_session
from app.users import models, utils
from app.users.schemas import UserCreate, UserOut, Token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

@router.post("/signup", response_model=UserOut)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    existing_user = await db.execute(
        select(models.User).filter(models.User.name == user_data.name)
    )
    if existing_user.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = utils.hash_password(user_data.password)
    db_user = models.User(
        name=user_data.name,
        password_hash=hashed_password,
        phone=user_data.phone
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_query = await db.execute(
        select(models.User).filter(models.User.name == form_data.username)
    )
    user = user_query.scalar()

    if not user or not utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.name},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_query = await db.execute(
        select(models.User).filter(models.User.name == name)
    )
    user = user_query.scalar()
    if user is None:
        raise credentials_exception
    return user
