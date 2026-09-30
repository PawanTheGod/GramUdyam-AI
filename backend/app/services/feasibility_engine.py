"""
GramUdyam AI – Deterministic Feasibility Engine
=================================================

Feasibility Score =
    0.25 × Capital Fit
  + 0.20 × Local Demand
  + 0.15 × Competition (inverse)
  + 0.15 × Expected Profit
  + 0.10 × Skill Fit
  + 0.10 × Seasonality
  + 0.05 × Infrastructure

Each factor is normalized to 0-100.
"""

from typing import List, Dict, Optional, Tuple
from app.models import BusinessOpportunity, FarmerProfile, LocalMarketData

WEIGHTS = {
    "capital_fit": 0.25,
    "demand": 0.20,
    "competition": 0.15,
    "profit": 0.15,
    "skill_fit": 0.10,
    "seasonality": 0.10,
    "infrastructure": 0.05,
}

INFRA_SCORES = {"Good": 85, "Medium": 55, "Poor": 25}
RISK_MAP = {"Low": 80, "Medium": 55, "High": 30}


def _clamp(v: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, v))


def compute_capital_fit(
    user_capital: float,
    invest_min: float,
    invest_max: float,
) -> float:
    """100 if user has enough capital for max investment, scales down."""
    if invest_min <= 0:
        return 80.0
    if user_capital >= invest_max:
        return 95.0
    if user_capital >= invest_min:
        ratio = (user_capital - invest_min) / max(invest_max - invest_min, 1)
        return _clamp(60 + ratio * 35)
    # under-capitalized
    ratio = user_capital / invest_min
    return _clamp(ratio * 55)


def compute_demand_score(
    business: BusinessOpportunity,
    market_data: Optional[LocalMarketData],
) -> float:
    """Combines base demand with district-level competitor density."""
    base = business.local_demand_base * 100  # 0-100
    if market_data and market_data.competitor_density:
        cat = business.category.lower()
        density = market_data.competitor_density.get(cat, 0.5)
        # lower density → higher opportunity
        adjustment = (1 - density) * 20
        base = _clamp(base + adjustment)
    return base


def compute_competition_score(
    business: BusinessOpportunity,
    market_data: Optional[LocalMarketData],
) -> float:
    """Inverse of competition — high score means low competition."""
    base_comp = business.competition_base  # 0-1
    if market_data and market_data.competitor_density:
        cat = business.category.lower()
        density = market_data.competitor_density.get(cat, 0.5)
        base_comp = (base_comp + density) / 2
    return _clamp((1 - base_comp) * 100)


def compute_profit_score(business: BusinessOpportunity) -> float:
    """Based on profit margin and absolute profit."""
    if business.expected_monthly_revenue <= 0:
        return 20.0
    margin = business.estimated_monthly_profit / business.expected_monthly_revenue
    # Combine margin (0-1 → 0-60) with absolute profit bonus
    profit_k = business.estimated_monthly_profit / 1000
    absolute_bonus = min(profit_k * 2, 40)
    return _clamp(margin * 60 + absolute_bonus)


def compute_skill_fit(
    business: BusinessOpportunity,
    profile: FarmerProfile,
) -> float:
    """Matches user skills against required skills."""
    required = set()
    if business.required_skills:
        required = {s.strip().lower() for s in business.required_skills.split(",")}
    if not required:
        return 70.0  # no specific skill required = fairly accessible

    user_skills = set()
    if profile.skills:
        user_skills = {s.strip().lower() for s in profile.skills.split(",")}
    if not user_skills:
        return 35.0  # user has no listed skills

    matches = required.intersection(user_skills)
    ratio = len(matches) / len(required)
    return _clamp(30 + ratio * 70)


def compute_seasonality_score(business: BusinessOpportunity) -> float:
    """Higher factor = more year-round viability."""
    return _clamp(business.seasonality_factor * 100)


def compute_infrastructure_score(
    business: BusinessOpportunity,
    market_data: Optional[LocalMarketData],
) -> float:
    """Based on road, electricity, internet connectivity."""
    if not market_data:
        return 50.0
    road = INFRA_SCORES.get(market_data.road_connectivity, 50)
    elec = INFRA_SCORES.get(market_data.electricity_reliability, 50)
    net = INFRA_SCORES.get(market_data.internet_connectivity, 50)
    bank = INFRA_SCORES.get(market_data.banking_access, 50)

    infra_req = business.infrastructure_requirement
    if infra_req == "Low":
        # business doesn't need much infra — score higher regardless
        return _clamp((road * 0.4 + elec * 0.3 + bank * 0.3) * 1.1)
    elif infra_req == "High":
        return _clamp((road * 0.25 + elec * 0.25 + net * 0.25 + bank * 0.25) * 0.9)
    else:
        return _clamp(road * 0.3 + elec * 0.3 + net * 0.2 + bank * 0.2)


def classify(score: float) -> str:
    if score >= 70:
        return "High"
    elif score >= 45:
        return "Medium"
    return "Low"


def generate_explanation(
    business: BusinessOpportunity,
    scores: Dict[str, float],
    total: float,
    classification: str,
    profile: FarmerProfile,
) -> Tuple[str, List[str], List[str]]:
    """Generate explanation, positive factors, and risk factors."""
    positives = []
    risks = []

    if scores["capital_fit"] >= 70:
        positives.append(f"Your available capital (₹{profile.available_capital:,.0f}) fits well within the investment range.")
    elif scores["capital_fit"] < 40:
        risks.append(f"Your capital (₹{profile.available_capital:,.0f}) may be insufficient. Consider loan support.")

    if scores["demand"] >= 65:
        positives.append(f"Strong local demand for {business.name} in your district.")
    elif scores["demand"] < 40:
        risks.append("Local demand appears limited. Market development may be needed.")

    if scores["competition"] >= 65:
        positives.append("Low competition in your area creates a market opportunity.")
    elif scores["competition"] < 40:
        risks.append("High competition exists. Differentiation strategy needed.")

    if scores["profit"] >= 60:
        positives.append(f"Good profit potential: ₹{business.estimated_monthly_profit:,.0f}/month expected.")
    elif scores["profit"] < 35:
        risks.append("Profit margins are thin. Cost management is critical.")

    if scores["skill_fit"] >= 60:
        positives.append("Your skills align well with this business.")
    elif scores["skill_fit"] < 40:
        risks.append("Skills gap identified. Training recommended before starting.")

    if scores["seasonality"] >= 70:
        positives.append("Year-round income potential with low seasonal variation.")
    elif scores["seasonality"] < 40:
        risks.append("Highly seasonal business. Plan for off-season income.")

    if scores["infrastructure"] >= 60:
        positives.append("Local infrastructure supports this business type.")
    elif scores["infrastructure"] < 40:
        risks.append("Infrastructure limitations may increase operating challenges.")

    explanation = (
        f"{business.name} received a feasibility score of {total:.1f}/100 ({classification}). "
    )
    if positives:
        explanation += f"Key strengths: {'; '.join(positives[:3])}. "
    if risks:
        explanation += f"Key risks: {'; '.join(risks[:3])}."

    return explanation, positives, risks


def generate_why_recommended(
    business: BusinessOpportunity,
    scores: Dict[str, float],
    total: float,
    profile: FarmerProfile,
) -> str:
    """Generate a reason for why this business is recommended."""
    reasons = []
    if scores["capital_fit"] >= 60:
        reasons.append(f"fits your budget of ₹{profile.available_capital:,.0f}")
    if scores["demand"] >= 60:
        reasons.append("has strong local demand")
    if scores["competition"] >= 60:
        reasons.append("faces low competition in your area")
    if scores["profit"] >= 55:
        reasons.append(f"offers good profit potential (₹{business.estimated_monthly_profit:,.0f}/mo)")
    if scores["skill_fit"] >= 55:
        reasons.append("matches your skillset")
    if scores["seasonality"] >= 60:
        reasons.append("provides year-round income")

    if not reasons:
        reasons.append("is a viable option for your profile")

    return f"{business.name} is recommended because it {', '.join(reasons[:4])}."


def analyze_single_business(
    business: BusinessOpportunity,
    profile: FarmerProfile,
    market_data: Optional[LocalMarketData],
) -> Dict:
    """Run feasibility analysis for a single business against a farmer profile."""

    scores = {
        "capital_fit": compute_capital_fit(
            profile.available_capital,
            business.required_investment_min,
            business.required_investment_max,
        ),
        "demand": compute_demand_score(business, market_data),
        "competition": compute_competition_score(business, market_data),
        "profit": compute_profit_score(business),
        "skill_fit": compute_skill_fit(business, profile),
        "seasonality": compute_seasonality_score(business),
        "infrastructure": compute_infrastructure_score(business, market_data),
    }

    total = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    total = _clamp(total)
    classification = classify(total)

    explanation, positives, risks = generate_explanation(
        business, scores, total, classification, profile
    )
    why = generate_why_recommended(business, scores, total, profile)

    demand_level = "High" if scores["demand"] >= 65 else ("Medium" if scores["demand"] >= 40 else "Low")
    avg_investment = (business.required_investment_min + business.required_investment_max) / 2

    return {
        "business_id": business.id,
        "business_name": business.name,
        "feasibility_score": round(total, 1),
        "classification": classification,
        "capital_fit_score": round(scores["capital_fit"], 1),
        "demand_score": round(scores["demand"], 1),
        "competition_score": round(scores["competition"], 1),
        "profit_score": round(scores["profit"], 1),
        "skill_fit_score": round(scores["skill_fit"], 1),
        "seasonality_score": round(scores["seasonality"], 1),
        "infrastructure_score": round(scores["infrastructure"], 1),
        "positive_factors": positives,
        "risk_factors": risks,
        "explanation": explanation,
        "required_investment": avg_investment,
        "expected_profit": business.estimated_monthly_profit,
        "break_even_months": business.break_even_months,
        "demand_level": demand_level,
        "risk_level": business.risk_level,
        "why_recommended": why,
    }


def analyze_all_businesses(
    businesses: List[BusinessOpportunity],
    profile: FarmerProfile,
    market_data: Optional[LocalMarketData],
    top_n: int = 3,
) -> List[Dict]:
    """Analyze all businesses and return top N recommendations sorted by score."""
    results = []
    for biz in businesses:
        result = analyze_single_business(biz, profile, market_data)
        results.append(result)

    results.sort(key=lambda x: x["feasibility_score"], reverse=True)
    return results[:top_n]
