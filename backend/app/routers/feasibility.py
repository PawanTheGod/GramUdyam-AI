from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import User, FarmerProfile, BusinessOpportunity, LocalMarketData, FeasibilityAssessment
from app.schemas import FeasibilityRequest, FeasibilityResponse, FeasibilityScoreDetail
from app.auth import require_user
from app.services.feasibility_engine import analyze_single_business, analyze_all_businesses

router = APIRouter(prefix="/api/feasibility", tags=["Feasibility"])


@router.post("/analyze", response_model=FeasibilityResponse)
def analyze_feasibility(
    request: FeasibilityRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    # Get farmer profile
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == request.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Farmer profile not found. Create a profile first.")

    # Get local market data
    market_data = db.query(LocalMarketData).filter(
        LocalMarketData.district.ilike(f"%{request.district}%")
    ).first()

    assessment_ids = []

    if request.business_id:
        # Analyze a single business
        business = db.query(BusinessOpportunity).filter(
            BusinessOpportunity.id == request.business_id
        ).first()
        if not business:
            raise HTTPException(status_code=404, detail="Business not found.")

        result = analyze_single_business(business, profile, market_data)
        results = [result]
    else:
        # Analyze all businesses
        businesses = db.query(BusinessOpportunity).filter(
            BusinessOpportunity.is_active == True
        ).all()
        results = analyze_all_businesses(businesses, profile, market_data, top_n=8)

    # Save assessments to DB
    for r in results:
        assessment = FeasibilityAssessment(
            user_id=request.user_id,
            business_id=r["business_id"],
            district=request.district,
            feasibility_score=r["feasibility_score"],
            classification=r["classification"],
            capital_fit_score=r["capital_fit_score"],
            demand_score=r["demand_score"],
            competition_score=r["competition_score"],
            profit_score=r["profit_score"],
            skill_fit_score=r["skill_fit_score"],
            seasonality_score=r["seasonality_score"],
            infrastructure_score=r["infrastructure_score"],
            positive_factors=r["positive_factors"],
            risk_factors=r["risk_factors"],
            explanation=r["explanation"],
        )
        db.add(assessment)
        db.flush()
        assessment_ids.append(assessment.id)

    db.commit()

    recommendations = [FeasibilityScoreDetail(**r) for r in results]

    return FeasibilityResponse(
        user_id=request.user_id,
        district=request.district,
        recommendations=recommendations,
        assessment_ids=assessment_ids,
        timestamp=datetime.utcnow(),
    )


@router.get("/assessments/{user_id}")
def get_user_assessments(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    assessments = db.query(FeasibilityAssessment).filter(
        FeasibilityAssessment.user_id == user_id
    ).order_by(FeasibilityAssessment.created_at.desc()).limit(20).all()

    results = []
    for a in assessments:
        biz = db.query(BusinessOpportunity).filter(BusinessOpportunity.id == a.business_id).first()
        results.append({
            "id": a.id,
            "business_name": biz.name if biz else "Unknown",
            "business_id": a.business_id,
            "district": a.district,
            "feasibility_score": a.feasibility_score,
            "classification": a.classification,
            "positive_factors": a.positive_factors,
            "risk_factors": a.risk_factors,
            "explanation": a.explanation,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        })
    return results
