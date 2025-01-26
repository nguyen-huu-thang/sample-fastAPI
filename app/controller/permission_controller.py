# app/controller/permission.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.permission_schema import PermissionCreate, PermissionRead
from app.service.permission_service import create_new_permission, fetch_permission_by_id
from app.configuration.database import get_db

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.post("/", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
async def create_permission(permission: PermissionCreate, db: AsyncSession = Depends(get_db)):
    return await create_new_permission(db, permission)

@router.get("/{permission_id}", response_model=PermissionRead)
async def get_permission(permission_id: int, db: AsyncSession = Depends(get_db)):
    permission = await fetch_permission_by_id(db, permission_id)
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return permission
