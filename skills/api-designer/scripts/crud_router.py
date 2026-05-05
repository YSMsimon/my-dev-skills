from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/v1/users", tags=["users"])


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    role: str = "member"


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    created_at: datetime


@router.post("", response_model=UserResponse, status_code=201)
def create_user(body: CreateUserRequest, db=Depends(get_db)):
    if db.user_exists(body.email):
        raise HTTPException(status_code=409, detail={
            "error": {"code": "EMAIL_ALREADY_EXISTS", "message": "Email already in use"}
        })
    return db.create_user(body.email, body.name, body.role)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db=Depends(get_db)):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail={
            "error": {"code": "USER_NOT_FOUND", "message": f"User {user_id} not found"}
        })
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, body: UpdateUserRequest, db=Depends(get_db),
                current_user=Depends(get_current_user)):
    if current_user != user_id and not is_admin(current_user):
        raise HTTPException(status_code=403, detail={
            "error": {"code": "FORBIDDEN", "message": "Cannot update another user's profile"}
        })
    updates = body.dict(exclude_none=True)
    return db.update_user(user_id, updates)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, db=Depends(get_db)):
    db.delete_user(user_id)
