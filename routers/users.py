from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User as UserModel, Role as RoleModel
from schemas import UserCreate, UserRead, UserUpdate, LoginRequest
from config import pwd_context
from security import create_access_token

router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = UserModel(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    """Obtener una lista de usuarios"""
    users = db.query(UserModel).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener un usuario por ID.
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return db_user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Modificar información de un usuario.
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if user_update.username is not None:
        existing_user = db.query(UserModel).filter(UserModel.username == user_update.username).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso",
            )
        db_user.username = user_update.username

    if user_update.password is not None:
        db_user.hashed_password = pwd_context.hash(user_update.password)

    if user_update.role is not None:
        if user_update.role not in [RoleModel.USER, RoleModel.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rol inválido"
            )
        db_user.role = user_update.role

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un usuario por ID.
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    db.delete(db_user)
    db.commit()
    return


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    """
    Validar las credenciales de un usuario.
    """
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas."
        )

    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas."
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role
    }

