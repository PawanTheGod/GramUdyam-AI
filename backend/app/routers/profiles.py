from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import User, FarmerProfile
from app.schemas import FarmerProfileCreate, FarmerProfileResponse
from app.auth import require_user

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])


@router.post("", response_model=FarmerProfileResponse)
def create_or_update_profile(
    profile_data: FarmerProfileCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    existing = db.query(FarmerProfile).filter(FarmerProfile.user_id == user.id).first()

    if existing:
        for key, value in profile_data.model_dump().items():
            setattr(existing, key, value)
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing

    profile = FarmerProfile(user_id=user.id, **profile_data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("", response_model=FarmerProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create your profile first.")
    return profile


@router.get("/{user_id}", response_model=FarmerProfileResponse)
def get_profile_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return profile
