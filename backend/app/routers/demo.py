"""
One-click demo scenario that runs the complete pipeline:
Profile → Local Data → Business Analysis → Feasibility → Financial → Schemes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import (
    User, FarmerProfile, BusinessOpportunity, LocalMarketData,
    FeasibilityAssessment, FinancialPlan, GovernmentScheme
)
from app.schemas import (
    DemoScenarioRequest, DemoScenarioResponse,
    FarmerProfileResponse, LocalMarketDataResponse,
    FeasibilityScoreDetail, FinancialPlanResponse, SchemeResponse
)
from app.auth import require_user
from app.services.feasibility_engine import analyze_all_businesses
from app.services.financial_calculator import generate_financial_plan
from app.services.scheme_matcher import match_schemes

router = APIRouter(prefix="/api/demo", tags=["Demo Scenario"])


@router.post("/run-assessment", response_model=DemoScenarioResponse)
def run_demo_assessment(
    request: DemoScenarioRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    """Execute the complete assessment pipeline in one call."""

    # ── 1. Create/Update Profile ──────────────────────────────────
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == user.id).first()
    if not profile:
        profile = FarmerProfile(
            user_id=user.id,
            name=user.full_name,
            village=request.village,
            block=request.village,
            district=request.district,
            state=request.state,
            available_capital=request.capital,
            business_interest=request.interest,
            available_land=1.0,
            skills="agriculture,animal care,basic accounting",
            preferred_language=request.language,
        )
        db.add(profile)
    else:
        profile.village = request.village
        profile.block = request.village
        profile.district = request.district
        profile.state = request.state
        profile.available_capital = request.capital
        profile.business_interest = request.interest
        profile.preferred_language = request.language
        profile.updated_at = datetime.utcnow()

    db.flush()

    # ── 2. Get Local Data ─────────────────────────────────────────
    market_data = db.query(LocalMarketData).filter(
        LocalMarketData.district.ilike(f"%{request.district}%")
    ).first()

    # ── 3. Analyze All Businesses ─────────────────────────────────
    businesses = db.query(BusinessOpportunity).filter(
        BusinessOpportunity.is_active == True
    ).all()

    results = analyze_all_businesses(businesses, profile, market_data, top_n=3)

    # ── 4. Save Assessments ───────────────────────────────────────
    assessment_ids = []
    for r in results:
        assessment = FeasibilityAssessment(
            user_id=user.id,
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

    # ── 5. Financial Plan for Top Recommendation ──────────────────
    top_biz_id = results[0]["business_id"]
    top_biz = db.query(BusinessOpportunity).filter(
        BusinessOpportunity.id == top_biz_id
    ).first()

    project_cost = (top_biz.required_investment_min + top_biz.required_investment_max) / 2
    fin_data = generate_financial_plan(
        project_cost=project_cost,
        user_contribution=request.capital,
        expected_monthly_revenue=top_biz.expected_monthly_revenue,
        monthly_operating_cost=top_biz.estimated_monthly_cost,
    )

    fin_plan = FinancialPlan(assessment_id=assessment_ids[0], **fin_data)
    db.add(fin_plan)
    db.flush()

    # ── 6. Scheme Matching ────────────────────────────────────────
    all_schemes = db.query(GovernmentScheme).filter(
        GovernmentScheme.is_active == True
    ).all()
    scheme_result = match_schemes(
        all_schemes, top_biz.category, request.district, request.capital, request.state
    )

    db.commit()
    db.refresh(profile)
    db.refresh(fin_plan)

    # ── Build Response ────────────────────────────────────────────
    recommendations = [FeasibilityScoreDetail(**r) for r in results]
    matched_schemes = [
        SchemeResponse.model_validate(s, from_attributes=True)
        for s in scheme_result["matched_schemes"]
    ]

    summary = (
        f"Assessment complete for {request.village}, {request.district}. "
        f"Top recommendation: {results[0]['business_name']} with a feasibility score of "
        f"{results[0]['feasibility_score']}/100 ({results[0]['classification']}). "
        f"Estimated monthly profit: Rs. {fin_data['monthly_profit']:,.0f} after EMI. "
        f"Matched {len(matched_schemes)} government scheme(s)."
    )

    return DemoScenarioResponse(
        profile=FarmerProfileResponse.model_validate(profile, from_attributes=True),
        local_data=LocalMarketDataResponse.model_validate(market_data, from_attributes=True) if market_data else None,
        recommendations=recommendations,
        financial_plan=FinancialPlanResponse.model_validate(fin_plan, from_attributes=True),
        matched_schemes=matched_schemes,
        summary=summary,
    )
