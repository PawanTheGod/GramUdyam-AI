from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import DemoLoginRequest, TokenResponse
from app.auth import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


DEMO_USERS = {
    "farmer": {"username": "demo_farmer", "full_name": "Demo Farmer", "role": "farmer"},
    "officer": {"username": "demo_officer", "full_name": "District Officer", "role": "officer"},
    "admin": {"username": "demo_admin", "full_name": "System Admin", "role": "admin"},
}


@router.post("/demo-login", response_model=TokenResponse)
def demo_login(request: DemoLoginRequest, db: Session = Depends(get_db)):
    role = request.role.lower()
    if role not in DEMO_USERS:
        role = "farmer"

    user_info = DEMO_USERS[role]
    user = db.query(User).filter(User.username == user_info["username"]).first()

    if not user:
        user = User(**user_info, language=request.language)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.language = request.language
        db.commit()

    token = create_access_token(data={"sub": user.id, "role": user.role})

    return TokenResponse(
        access_token=token,
        user={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "language": user.language,
        },
    )
