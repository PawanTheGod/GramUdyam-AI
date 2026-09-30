"""
GramUdyam AI – Government Scheme Matcher
==========================================

Matches government schemes against user profile and selected business.
"""

from typing import List, Dict
from app.models import GovernmentScheme, FarmerProfile


def match_schemes(
    schemes: List[GovernmentScheme],
    business_category: str,
    district: str,
    user_capital: float = 0,
    state: str = "Maharashtra",
) -> Dict:
    """Match schemes to business category and user profile."""
    matched = []
    total_support = 0.0
    category_lower = business_category.lower()

    for scheme in schemes:
        if not scheme.is_active:
            continue

        eligible_cats = scheme.eligible_categories or []
        # Check category match
        cat_match = any(
            category_lower in cat.lower() or cat.lower() in category_lower
            for cat in eligible_cats
        )

        # Also match if scheme is for "all" or "general"
        general_match = any(
            cat.lower() in ("all", "general", "agriculture", "rural")
            for cat in eligible_cats
        )

        # State match
        state_match = (
            scheme.scheme_type == "Central"
            or state.lower() in (scheme.department or "").lower()
            or scheme.scheme_type == "State"  # assume state schemes match for demo
        )

        if (cat_match or general_match) and state_match:
            matched.append(scheme)
            if scheme.max_support:
                total_support += scheme.max_support

    # Sort by max support descending
    matched.sort(key=lambda s: s.max_support or 0, reverse=True)

    # Generate recommendation
    if total_support > 0:
        recommendation = (
            f"You may be eligible for up to ₹{total_support:,.0f} in total support across "
            f"{len(matched)} government scheme(s). Apply through the respective department portals."
        )
    elif matched:
        recommendation = (
            f"Found {len(matched)} potentially applicable scheme(s). "
            "Contact your nearest Krishi Seva Kendra or District Industry Centre for details."
        )
    else:
        recommendation = (
            "No directly matching schemes found for this business category. "
            "Check with the District Industry Centre for the latest schemes."
        )

    return {
        "matched_schemes": matched,
        "total_potential_support": total_support,
        "recommendation": recommendation,
    }
