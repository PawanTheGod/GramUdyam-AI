from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import GovernmentScheme
from app.schemas import SchemeResponse, SchemeMatchRequest, SchemeMatchResponse
from app.services.scheme_matcher import match_schemes

router = APIRouter(prefix="/api/schemes", tags=["Government Schemes"])


@router.get("", response_model=list[SchemeResponse])
def list_schemes(db: Session = Depends(get_db)):
    return db.query(GovernmentScheme).filter(GovernmentScheme.is_active == True).all()


@router.post("/match", response_model=SchemeMatchResponse)
def match_user_schemes(
    request: SchemeMatchRequest,
    db: Session = Depends(get_db),
):
    all_schemes = db.query(GovernmentScheme).filter(
        GovernmentScheme.is_active == True
    ).all()

    result = match_schemes(
        schemes=all_schemes,
        business_category=request.business_category,
        district=request.district,
        user_capital=request.user_capital,
        state=request.state,
    )

    return SchemeMatchResponse(
        matched_schemes=[SchemeResponse.model_validate(s, from_attributes=True) for s in result["matched_schemes"]],
        total_potential_support=result["total_potential_support"],
        recommendation=result["recommendation"],
    )
