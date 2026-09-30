from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import (
    User, FarmerProfile, FeasibilityAssessment, FinancialPlan,
    BusinessOpportunity, LocalMarketData, GovernmentScheme
)
from app.schemas import DashboardResponse, AdminDashboardResponse
from app.auth import require_user, require_role

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    # Profile
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == user.id).first()

    # Recent assessments
    assessments = db.query(FeasibilityAssessment).filter(
        FeasibilityAssessment.user_id == user.id
    ).order_by(FeasibilityAssessment.created_at.desc()).limit(10).all()

    recent = []
    top_recs = []
    for a in assessments:
        biz = db.query(BusinessOpportunity).filter(BusinessOpportunity.id == a.business_id).first()
        entry = {
            "id": a.id,
            "business_name": biz.name if biz else "Unknown",
            "business_name_hi": biz.name_hi if biz else None,
            "business_name_mr": biz.name_mr if biz else None,
            "business_id": a.business_id,
            "category": biz.category if biz else "",
            "district": a.district,
            "feasibility_score": a.feasibility_score,
            "classification": a.classification,
            "positive_factors": a.positive_factors,
            "risk_factors": a.risk_factors,
            "explanation": a.explanation,
            "expected_profit": biz.estimated_monthly_profit if biz else 0,
            "required_investment": (biz.required_investment_min + biz.required_investment_max) / 2 if biz else 0,
            "break_even_months": biz.break_even_months if biz else 0,
            "risk_level": biz.risk_level if biz else "Medium",
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        recent.append(entry)
        if a.feasibility_score >= 50 and len(top_recs) < 3:
            top_recs.append(entry)

    # Market summary
    market_summary = None
    if profile:
        market = db.query(LocalMarketData).filter(
            LocalMarketData.district.ilike(f"%{profile.district}%")
        ).first()
        if market:
            market_summary = {
                "district": market.district,
                "population": market.population,
                "road_connectivity": market.road_connectivity,
                "market_prices": market.market_prices,
                "seasonal_demand": market.seasonal_demand,
                "existing_businesses": market.existing_businesses,
            }

    # Financial summary from latest plan
    financial_summary = None
    if assessments:
        latest_plan = db.query(FinancialPlan).filter(
            FinancialPlan.assessment_id == assessments[0].id
        ).first()
        if latest_plan:
            financial_summary = {
                "project_cost": latest_plan.project_cost,
                "loan_amount": latest_plan.loan_amount,
                "emi": latest_plan.emi,
                "monthly_profit": latest_plan.monthly_profit,
                "annual_income": latest_plan.annual_income,
                "break_even_months": latest_plan.break_even_months,
                "roi_percentage": latest_plan.roi_percentage,
            }

    # Matched schemes count
    matched_count = 0
    if profile and assessments:
        biz = db.query(BusinessOpportunity).filter(
            BusinessOpportunity.id == assessments[0].business_id
        ).first()
        if biz:
            from app.services.scheme_matcher import match_schemes
            all_schemes = db.query(GovernmentScheme).filter(GovernmentScheme.is_active == True).all()
            result = match_schemes(all_schemes, biz.category, profile.district)
            matched_count = len(result["matched_schemes"])

    return DashboardResponse(
        profile=profile,
        recent_assessments=recent,
        top_recommendations=top_recs[:3],
        market_summary=market_summary,
        financial_summary=financial_summary,
        matched_schemes_count=matched_count,
        stats={
            "total_assessments": len(assessments),
            "avg_score": round(sum(a.feasibility_score for a in assessments) / len(assessments), 1) if assessments else 0,
        },
    )


@router.get("/admin", response_model=AdminDashboardResponse)
def get_admin_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    total_users = db.query(User).count()
    total_assessments = db.query(FeasibilityAssessment).count()

    # Unique businesses assessed
    businesses_assessed = db.query(
        func.count(func.distinct(FeasibilityAssessment.business_id))
    ).scalar() or 0

    # Feasibility distribution
    high = db.query(FeasibilityAssessment).filter(FeasibilityAssessment.classification == "High").count()
    medium = db.query(FeasibilityAssessment).filter(FeasibilityAssessment.classification == "Medium").count()
    low = db.query(FeasibilityAssessment).filter(FeasibilityAssessment.classification == "Low").count()

    # Popular categories
    popular = []
    biz_counts = db.query(
        BusinessOpportunity.category,
        func.count(FeasibilityAssessment.id)
    ).join(
        FeasibilityAssessment,
        FeasibilityAssessment.business_id == BusinessOpportunity.id
    ).group_by(BusinessOpportunity.category).all()

    for cat, count in biz_counts:
        popular.append({"category": cat, "count": count})
    popular.sort(key=lambda x: x["count"], reverse=True)

    # District assessments
    district_counts = db.query(
        FeasibilityAssessment.district,
        func.count(FeasibilityAssessment.id)
    ).group_by(FeasibilityAssessment.district).all()

    district_assessments = [{"district": d, "count": c} for d, c in district_counts]

    return AdminDashboardResponse(
        total_users=total_users,
        total_assessments=total_assessments,
        businesses_assessed=businesses_assessed,
        feasibility_distribution={"High": high, "Medium": medium, "Low": low},
        popular_categories=popular,
        district_assessments=district_assessments,
        system_status={
            "database": "connected",
            "version": "1.0.0-mvp",
            "data_type": "demo",
            "districts_available": 3,
            "businesses_available": db.query(BusinessOpportunity).count(),
            "schemes_available": db.query(GovernmentScheme).count(),
        },
    )
