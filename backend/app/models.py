from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False, default="farmer")  # farmer, officer, admin
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    profile = relationship("FarmerProfile", back_populates="user", uselist=False)
    assessments = relationship("FeasibilityAssessment", back_populates="user")


class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    village = Column(String(200))
    block = Column(String(200))
    district = Column(String(200), nullable=False)
    state = Column(String(200), nullable=False, default="Maharashtra")
    available_capital = Column(Float, default=0)
    business_interest = Column(String(500))
    available_land = Column(Float, default=0)  # in acres
    skills = Column(Text)  # comma-separated
    preferred_language = Column(String(10), default="en")
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class BusinessOpportunity(Base):
    __tablename__ = "business_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    name_hi = Column(String(200))
    name_mr = Column(String(200))
    category = Column(String(100), nullable=False)
    description = Column(Text)
    description_hi = Column(Text)
    description_mr = Column(Text)
    required_investment_min = Column(Float, nullable=False)
    required_investment_max = Column(Float, nullable=False)
    expected_monthly_revenue = Column(Float, nullable=False)
    estimated_monthly_cost = Column(Float, nullable=False)
    estimated_monthly_profit = Column(Float, nullable=False)
    break_even_months = Column(Integer, nullable=False)
    required_land = Column(Float, default=0)  # in acres
    required_skills = Column(Text)  # comma-separated
    risk_level = Column(String(20), default="Medium")  # Low, Medium, High
    seasonality_factor = Column(Float, default=0.7)  # 0-1
    infrastructure_requirement = Column(String(20), default="Medium")
    local_demand_base = Column(Float, default=0.6)  # 0-1
    competition_base = Column(Float, default=0.5)  # 0-1
    is_active = Column(Boolean, default=True)


class LocalMarketData(Base):
    __tablename__ = "local_market_data"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String(200), nullable=False, index=True)
    state = Column(String(200), nullable=False, default="Maharashtra")
    population = Column(Integer)
    num_villages = Column(Integer)
    existing_businesses = Column(JSON)  # {category: count}
    competitor_density = Column(JSON)  # {category: density_score}
    market_prices = Column(JSON)  # {product: price}
    seasonal_demand = Column(JSON)  # {month: demand_factor}
    nearby_towns = Column(JSON)  # [{name, distance_km, population}]
    road_connectivity = Column(String(20), default="Medium")  # Good, Medium, Poor
    internet_connectivity = Column(String(20), default="Medium")
    banking_access = Column(String(20), default="Medium")
    electricity_reliability = Column(String(20), default="Medium")
    cold_storage_available = Column(Boolean, default=False)
    mandi_distance_km = Column(Float, default=20)
    is_demo_data = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow)


class GovernmentScheme(Base):
    __tablename__ = "government_schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    name_hi = Column(String(300))
    name_mr = Column(String(300))
    scheme_type = Column(String(50), nullable=False)  # Central, State
    department = Column(String(200))
    eligible_categories = Column(JSON)  # list of business categories
    max_support = Column(Float)
    support_type = Column(String(100))  # Subsidy, Loan, Grant
    subsidy_percentage = Column(Float)
    eligibility_criteria = Column(Text)
    required_documents = Column(JSON)  # list of documents
    description = Column(Text)
    description_hi = Column(Text)
    description_mr = Column(Text)
    application_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_demo_data = Column(Boolean, default=True)


class FeasibilityAssessment(Base):
    __tablename__ = "feasibility_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    business_id = Column(Integer, ForeignKey("business_opportunities.id"), nullable=False)
    district = Column(String(200), nullable=False)
    feasibility_score = Column(Float, nullable=False)
    classification = Column(String(20), nullable=False)  # High, Medium, Low
    capital_fit_score = Column(Float)
    demand_score = Column(Float)
    competition_score = Column(Float)
    profit_score = Column(Float)
    skill_fit_score = Column(Float)
    seasonality_score = Column(Float)
    infrastructure_score = Column(Float)
    positive_factors = Column(JSON)
    risk_factors = Column(JSON)
    explanation = Column(Text)
    explanation_hi = Column(Text)
    explanation_mr = Column(Text)
    recommendations = Column(JSON)  # top 3 recommended businesses
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessments")
    business = relationship("BusinessOpportunity")
    financial_plan = relationship("FinancialPlan", back_populates="assessment", uselist=False)


class FinancialPlan(Base):
    __tablename__ = "financial_plans"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("feasibility_assessments.id"), unique=True, nullable=False)
    project_cost = Column(Float, nullable=False)
    fixed_cost = Column(Float, nullable=False)
    working_capital = Column(Float, nullable=False)
    user_contribution = Column(Float, nullable=False)
    loan_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    emi = Column(Float, nullable=False)
    repayment_months = Column(Integer, nullable=False)
    expected_monthly_revenue = Column(Float, nullable=False)
    monthly_expenses = Column(Float, nullable=False)
    monthly_profit = Column(Float, nullable=False)
    break_even_months = Column(Integer, nullable=False)
    annual_income = Column(Float, nullable=False)
    roi_percentage = Column(Float)
    dscr = Column(Float)  # Debt Service Coverage Ratio
    created_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("FeasibilityAssessment", back_populates="financial_plan")
