from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, FeasibilityAssessment, BusinessOpportunity, FinancialPlan
from app.schemas import FinancialCalcRequest, FinancialPlanResponse
from app.auth import require_user
from app.services.financial_calculator import generate_financial_plan

router = APIRouter(prefix="/api/financial", tags=["Financial"])


@router.post("/calculate", response_model=FinancialPlanResponse)
def calculate_financial_plan(
    request: FinancialCalcRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    # Get assessment
    assessment = db.query(FeasibilityAssessment).filter(
        FeasibilityAssessment.id == request.assessment_id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")

    # Get business details
    business = db.query(BusinessOpportunity).filter(
        BusinessOpportunity.id == assessment.business_id
    ).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found.")

    # Calculate project cost as average of min/max investment
    project_cost = (business.required_investment_min + business.required_investment_max) / 2

    # User contribution
    from app.models import FarmerProfile
    profile = db.query(FarmerProfile).filter(FarmerProfile.user_id == assessment.user_id).first()
    user_contribution = request.user_contribution or (profile.available_capital if profile else 0)

    # Generate financial plan
    plan_data = generate_financial_plan(
        project_cost=project_cost,
        user_contribution=user_contribution,
        expected_monthly_revenue=business.expected_monthly_revenue,
        monthly_operating_cost=business.estimated_monthly_cost,
        interest_rate=request.loan_interest_rate,
        repayment_months=request.repayment_months,
    )

    # Check if plan exists for this assessment
    existing = db.query(FinancialPlan).filter(
        FinancialPlan.assessment_id == request.assessment_id
    ).first()

    if existing:
        for key, value in plan_data.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing

    plan = FinancialPlan(assessment_id=request.assessment_id, **plan_data)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/plan/{assessment_id}", response_model=FinancialPlanResponse)
def get_financial_plan(
    assessment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    plan = db.query(FinancialPlan).filter(
        FinancialPlan.assessment_id == assessment_id
    ).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Financial plan not found. Run the calculation first.")
    return plan
