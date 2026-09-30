from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────
class DemoLoginRequest(BaseModel):
    role: str = Field(..., description="One of: farmer, officer, admin")
    language: str = Field(default="en", description="en, hi, mr")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    language: str


# ── Farmer Profile ────────────────────────────────────────────────────
class FarmerProfileCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    village: Optional[str] = None
    block: Optional[str] = None
    district: str = Field(..., min_length=2, max_length=200)
    state: str = Field(default="Maharashtra", max_length=200)
    available_capital: float = Field(default=0, ge=0)
    business_interest: Optional[str] = None
    available_land: float = Field(default=0, ge=0)
    skills: Optional[str] = None
    preferred_language: str = Field(default="en")
    phone: Optional[str] = None

class FarmerProfileResponse(FarmerProfileCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Business ──────────────────────────────────────────────────────────
class BusinessOpportunityResponse(BaseModel):
    id: int
    name: str
    name_hi: Optional[str] = None
    name_mr: Optional[str] = None
    category: str
    description: Optional[str] = None
    description_hi: Optional[str] = None
    description_mr: Optional[str] = None
    required_investment_min: float
    required_investment_max: float
    expected_monthly_revenue: float
    estimated_monthly_cost: float
    estimated_monthly_profit: float
    break_even_months: int
    required_land: float
    required_skills: Optional[str] = None
    risk_level: str
    seasonality_factor: float
    infrastructure_requirement: str
    local_demand_base: float
    competition_base: float

    class Config:
        from_attributes = True


# ── Local Market Data ─────────────────────────────────────────────────
class LocalMarketDataResponse(BaseModel):
    id: int
    district: str
    state: str
    population: Optional[int] = None
    num_villages: Optional[int] = None
    existing_businesses: Optional[Dict] = None
    competitor_density: Optional[Dict] = None
    market_prices: Optional[Dict] = None
    seasonal_demand: Optional[Dict] = None
    nearby_towns: Optional[List] = None
    road_connectivity: str
    internet_connectivity: str
    banking_access: str
    electricity_reliability: str
    cold_storage_available: bool
    mandi_distance_km: float
    is_demo_data: bool

    class Config:
        from_attributes = True


# ── Feasibility ───────────────────────────────────────────────────────
class FeasibilityRequest(BaseModel):
    user_id: int
    district: str
    business_id: Optional[int] = None  # if None, analyze all businesses

class FeasibilityScoreDetail(BaseModel):
    business_id: int
    business_name: str
    feasibility_score: float
    classification: str
    capital_fit_score: float
    demand_score: float
    competition_score: float
    profit_score: float
    skill_fit_score: float
    seasonality_score: float
    infrastructure_score: float
    positive_factors: List[str]
    risk_factors: List[str]
    explanation: str
    explanation_hi: Optional[str] = None
    explanation_mr: Optional[str] = None
    required_investment: float
    expected_profit: float
    break_even_months: int
    demand_level: str
    risk_level: str
    why_recommended: str

class FeasibilityResponse(BaseModel):
    user_id: int
    district: str
    recommendations: List[FeasibilityScoreDetail]
    assessment_ids: List[int]
    timestamp: datetime


# ── Financial ─────────────────────────────────────────────────────────
class FinancialCalcRequest(BaseModel):
    assessment_id: int
    user_contribution: Optional[float] = None
    loan_interest_rate: float = Field(default=8.5, ge=0, le=30)
    repayment_months: int = Field(default=60, ge=12, le=240)

class FinancialPlanResponse(BaseModel):
    id: int
    assessment_id: int
    project_cost: float
    fixed_cost: float
    working_capital: float
    user_contribution: float
    loan_amount: float
    interest_rate: float
    emi: float
    repayment_months: int
    expected_monthly_revenue: float
    monthly_expenses: float
    monthly_profit: float
    break_even_months: int
    annual_income: float
    roi_percentage: Optional[float] = None
    dscr: Optional[float] = None

    class Config:
        from_attributes = True


# ── Schemes ───────────────────────────────────────────────────────────
class SchemeResponse(BaseModel):
    id: int
    name: str
    name_hi: Optional[str] = None
    name_mr: Optional[str] = None
    scheme_type: str
    department: Optional[str] = None
    eligible_categories: Optional[List] = None
    max_support: Optional[float] = None
    support_type: Optional[str] = None
    subsidy_percentage: Optional[float] = None
    eligibility_criteria: Optional[str] = None
    required_documents: Optional[List] = None
    description: Optional[str] = None
    description_hi: Optional[str] = None
    description_mr: Optional[str] = None
    is_demo_data: bool

    class Config:
        from_attributes = True

class SchemeMatchRequest(BaseModel):
    business_category: str
    district: str
    user_capital: float = 0
    state: str = "Maharashtra"

class SchemeMatchResponse(BaseModel):
    matched_schemes: List[SchemeResponse]
    total_potential_support: float
    recommendation: str


# ── Dashboard ─────────────────────────────────────────────────────────
class DashboardResponse(BaseModel):
    profile: Optional[FarmerProfileResponse] = None
    recent_assessments: List[dict] = []
    top_recommendations: List[dict] = []
    market_summary: Optional[dict] = None
    financial_summary: Optional[dict] = None
    matched_schemes_count: int = 0
    stats: dict = {}


# ── Admin ─────────────────────────────────────────────────────────────
class AdminDashboardResponse(BaseModel):
    total_users: int
    total_assessments: int
    businesses_assessed: int
    feasibility_distribution: Dict[str, int]
    popular_categories: List[dict]
    district_assessments: List[dict]
    system_status: dict


# ── Demo Scenario ─────────────────────────────────────────────────────
class DemoScenarioRequest(BaseModel):
    village: str = "Sangamner"
    district: str = "Ahmednagar"
    state: str = "Maharashtra"
    capital: float = 100000
    interest: str = "Rural/agricultural business"
    language: str = "mr"

class DemoScenarioResponse(BaseModel):
    profile: FarmerProfileResponse
    local_data: LocalMarketDataResponse
    recommendations: List[FeasibilityScoreDetail]
    financial_plan: Optional[FinancialPlanResponse] = None
    matched_schemes: List[SchemeResponse]
    summary: str
