from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.models.user import User


def require_role(allowed_roles: list[str]):
    """Check if user has required role."""
    
    async def checker(user: User = Depends(get_current_user)):
        if user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user
        
    return checker
