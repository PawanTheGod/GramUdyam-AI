from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import LocalMarketData
from app.schemas import LocalMarketDataResponse

router = APIRouter(prefix="/api/local-data", tags=["Local Data"])


@router.get("/{district}", response_model=LocalMarketDataResponse)
def get_local_data(district: str, db: Session = Depends(get_db)):
    data = db.query(LocalMarketData).filter(
        LocalMarketData.district.ilike(f"%{district}%")
    ).first()
    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"No local market data found for district: {district}. Demo data available for: Ahmednagar, Pune, Nashik."
        )
    return data


@router.get("", response_model=list[LocalMarketDataResponse])
def list_all_local_data(db: Session = Depends(get_db)):
    return db.query(LocalMarketData).all()
