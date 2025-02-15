from fastapi import APIRouter, HTTPException, Request, status
from app.core.security import user_context, authorization
from app.service.user_permission_service import UserPermissionService
from app.service.user_service import UserService
from app.schema.user_permission_schema import UserPermissionsAssign, UserPermissionsUpdate, UserPermissionsRead



router = APIRouter(prefix="/user-permissions", tags=["UserPermission"])

user_permission_service = UserPermissionService()
user_service = UserService()


@router.get("/{user_id}", response_model=UserPermissionsRead)
async def get_permissions_by_user(user_id: int):
    """
    Lấy danh sách tên quyền của người dùng theo user_id.
    
    Yêu cầu:
      - Người dùng cần đăng nhập để thực hiện hành động này.
      - User hiện tại phải có quyền "view_permissions".
    """
    user_current = user_context.get()
    if not user_current:
        raise HTTPException(status_code=401, detail="You have not logged in")
    # if not authorization_service.check_permission(user, "view_permissions"):
    #     raise HTTPException(status_code=403, detail="E2021")
    # try:
    target_user = await user_service.get_user_by_id(user_id)
    return await user_permission_service.get_permissions_by_user(target_user)


@router.post("", status_code=status.HTTP_201_CREATED)
async def assign_permission(user_permission: UserPermissionsAssign):
    """
    Gán (assign) quyền cho người dùng.
    
    Yêu cầu:
      - Người dùng cần đăng nhập để thực hiện hành động này.
      - User hiện tại phải có quyền "create_permission".
      - Payload JSON phải chứa các trường cần thiết, ví dụ:
      
            {
                "user_id": 123,
                "permissions": {
                    "permission_name_1": {"target": "all", "is_active": true, "is_denied": false},
                    "permission_name_2": {"target": 456, "is_active": true, "is_denied": true}
                }
            }
    """
    user_current = user_context.get()
    if not user_current:
        raise HTTPException(status_code=401, detail="You have not logged in")
    # if not authorization_service.check_permission(user, "create_permission"):
    #     raise HTTPException(status_code=403, detail="E2021")
    # try:
    assigned_permissions = await user_permission_service.assign_permissions(user_permission)
    return assigned_permissions
    # except Exception:
    #     raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@router.put("")
async def update_permission(data: UserPermissionsUpdate):
    """
    Cập nhật quyền của người dùng.
    
    Yêu cầu:
      - Người dùng cần đăng nhập để thực hiện hành động này.
      - User hiện tại phải có quyền "edit_permission".
      - Payload JSON phải chứa các trường cần thiết, ví dụ:
      
        {
            "user_id": 23,
            "permissions": [
                {
                "permission_id": 8,
                "target": 7
                },
                {
                "permission_id": 9,
                "target": 2
                }
            ]
        }
    """
    user_current = user_context.get()
    if not user_current:
        raise HTTPException(status_code=401, detail="You have not logged in")
    # if not authorization_service.check_permission(user, "edit_permission"):
    #     raise HTTPException(status_code=403, detail="E2021")
    updated_permissions = await user_permission_service.update_permission(data)
    return updated_permissions


@router.delete("")
async def delete_permission(request: Request):
    """
    Xóa quyền của người dùng.
    
    Yêu cầu:
      - Thông tin user phải có trong `request.state.user`.
      - User hiện tại phải có quyền "delete_permission".
      - Payload JSON phải chứa: user_id và danh sách permission names cần xóa, ví dụ:
      
            {
                "user_id": 123,
                "permissions": ["permission_name_1", "permission_name_2"]
            }
    """
    user_current = user_context.get()
    if not user_current:
        raise HTTPException(status_code=401, detail="You have not logged in")
    # if not authorization_service.check_permission(user, "delete_permission"):
    #     raise HTTPException(status_code=403, detail="E2021")
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # try:
    await user_permission_service.delete_permissions(data)
    return {"message": "Permissions deleted successfully."}
    # except AppException as e:
    #     raise HTTPException(status_code=400, detail=str(e))
