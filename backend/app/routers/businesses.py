from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import BusinessOpportunity
from app.schemas import BusinessOpportunityResponse

router = APIRouter(prefix="/api/businesses", tags=["Businesses"])


@router.get("", response_model=list[BusinessOpportunityResponse])
def list_businesses(
    category: str = None,
    db: Session = Depends(get_db),
):
    query = db.query(BusinessOpportunity).filter(BusinessOpportunity.is_active == True)
    if category:
        query = query.filter(BusinessOpportunity.category.ilike(f"%{category}%"))
    return query.all()


@router.get("/{business_id}", response_model=BusinessOpportunityResponse)
def get_business(business_id: int, db: Session = Depends(get_db)):
    biz = db.query(BusinessOpportunity).filter(BusinessOpportunity.id == business_id).first()
    if not biz:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Business not found.")
    return biz
