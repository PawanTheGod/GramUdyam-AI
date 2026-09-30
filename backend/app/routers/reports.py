"""
Report generation – produces a downloadable PDF feasibility report.
Uses fpdf2 for PDF generation.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from fpdf import FPDF
import os

from app.database import get_db
from app.models import (
    User, FarmerProfile, FeasibilityAssessment, FinancialPlan,
    BusinessOpportunity, LocalMarketData, GovernmentScheme
)
from app.auth import require_user
from app.services.scheme_matcher import match_schemes

router = APIRouter(prefix="/api/reports", tags=["Reports"])

# Path to a Unicode-capable font (bundled with the app)
FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "fonts")


class GramUdyamPDF(FPDF):
    """Custom PDF with GramUdyam branding."""

    def __init__(self):
        super().__init__()
        # Try to add a Unicode font if available, fallback to Helvetica
        try:
            font_path = os.path.join(FONT_DIR, "DejaVuSans.ttf")
            if os.path.exists(font_path):
                self.add_font("DejaVu", "", font_path, uni=True)
                self.add_font("DejaVu", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), uni=True)
                self._custom_font = "DejaVu"
            else:
                self._custom_font = None
        except Exception:
            self._custom_font = None

    def _use_font(self, style="", size=10):
        if self._custom_font:
            self.set_font(self._custom_font, style, size)
        else:
            self.set_font("Helvetica", style, size)

    def header(self):
        self._use_font("B", 16)
        self.set_text_color(21, 101, 52)
        self.cell(0, 10, "GramUdyam AI", border=0, ln=True, align="C")
        self._use_font("", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "AI-Powered Local Business Discovery, Feasibility & Financial Advisory", ln=True, align="C")
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self._use_font("", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  DEMO REPORT - For illustrative purposes only", align="C")

    def section_title(self, title):
        self._use_font("B", 13)
        self.set_text_color(21, 101, 52)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)
        self._use_font("", 10)

    def key_value(self, key, value):
        self._use_font("B", 10)
        self.cell(70, 7, f"{key}:", ln=False)
        self._use_font("", 10)
        # Sanitize value to handle encoding issues
        safe_value = str(value).encode('latin-1', 'replace').decode('latin-1') if not self._custom_font else str(value)
        self.cell(0, 7, safe_value, ln=True)


def _safe_text(text: str) -> str:
    """Ensure text is safe for PDF rendering."""
    if not text:
        return ""
    return text


@router.post("/generate")
def generate_report(
    assessment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    """Generate a downloadable PDF feasibility report."""

    assessment = db.query(FeasibilityAssessment).filter(
        FeasibilityAssessment.id == assessment_id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")

    profile = db.query(FarmerProfile).filter(
        FarmerProfile.user_id == assessment.user_id
    ).first()

    business = db.query(BusinessOpportunity).filter(
        BusinessOpportunity.id == assessment.business_id
    ).first()

    market = db.query(LocalMarketData).filter(
        LocalMarketData.district.ilike(f"%{assessment.district}%")
    ).first()

    fin_plan = db.query(FinancialPlan).filter(
        FinancialPlan.assessment_id == assessment_id
    ).first()

    all_schemes = db.query(GovernmentScheme).filter(GovernmentScheme.is_active == True).all()
    matched = match_schemes(
        all_schemes,
        business.category if business else "",
        assessment.district
    )

    # ── Build PDF ─────────────────────────────────────────────────
    pdf = GramUdyamPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title
    pdf._use_font("B", 18)
    pdf.set_text_color(21, 101, 52)
    pdf.cell(0, 12, "Feasibility Assessment Report", ln=True, align="C")
    pdf.ln(4)
    pdf._use_font("", 9)
    pdf.set_text_color(200, 50, 50)
    pdf.cell(0, 6, "DEMO DATA - This report uses illustrative data for demonstration purposes", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # ── 1. User Profile ───────────────────────────────────────────
    pdf.section_title("1. Applicant Profile")
    if profile:
        pdf.key_value("Name", profile.name)
        pdf.key_value("Village", profile.village or "N/A")
        pdf.key_value("Block", profile.block or "N/A")
        pdf.key_value("District", profile.district)
        pdf.key_value("State", profile.state)
        pdf.key_value("Available Capital", f"Rs. {profile.available_capital:,.0f}")
        pdf.key_value("Available Land", f"{profile.available_land} acres")
        pdf.key_value("Skills", profile.skills or "Not specified")
    pdf.ln(4)

    # ── 2. Selected Business ─────────────────────────────────────
    pdf.section_title("2. Business Opportunity")
    if business:
        pdf.key_value("Business", business.name)
        pdf.key_value("Category", business.category.title())
        pdf.key_value("Investment Range", f"Rs. {business.required_investment_min:,.0f} - Rs. {business.required_investment_max:,.0f}")
        pdf.key_value("Expected Monthly Revenue", f"Rs. {business.expected_monthly_revenue:,.0f}")
        pdf.key_value("Monthly Operating Cost", f"Rs. {business.estimated_monthly_cost:,.0f}")
        pdf.key_value("Expected Monthly Profit", f"Rs. {business.estimated_monthly_profit:,.0f}")
        pdf.key_value("Break-even Period", f"{business.break_even_months} months")
        pdf.key_value("Risk Level", business.risk_level)
    pdf.ln(4)

    # ── 3. Feasibility Score ──────────────────────────────────────
    pdf.section_title("3. Feasibility Analysis")
    pdf.key_value("Overall Score", f"{assessment.feasibility_score:.1f} / 100")
    pdf.key_value("Classification", assessment.classification)
    pdf.key_value("Capital Fit", f"{assessment.capital_fit_score:.1f}")
    pdf.key_value("Local Demand", f"{assessment.demand_score:.1f}")
    pdf.key_value("Competition (inverse)", f"{assessment.competition_score:.1f}")
    pdf.key_value("Profit Potential", f"{assessment.profit_score:.1f}")
    pdf.key_value("Skill Fit", f"{assessment.skill_fit_score:.1f}")
    pdf.key_value("Seasonality", f"{assessment.seasonality_score:.1f}")
    pdf.key_value("Infrastructure", f"{assessment.infrastructure_score:.1f}")
    pdf.ln(2)

    if assessment.positive_factors:
        pdf._use_font("B", 10)
        pdf.cell(0, 7, "Positive Factors:", ln=True)
        pdf._use_font("", 10)
        for f in (assessment.positive_factors or []):
            safe_f = f.encode('latin-1', 'replace').decode('latin-1') if not pdf._custom_font else f
            pdf.cell(10)
            pdf.multi_cell(0, 6, f"- {safe_f}")

    if assessment.risk_factors:
        pdf._use_font("B", 10)
        pdf.cell(0, 7, "Risk Factors:", ln=True)
        pdf._use_font("", 10)
        for f in (assessment.risk_factors or []):
            safe_f = f.encode('latin-1', 'replace').decode('latin-1') if not pdf._custom_font else f
            pdf.cell(10)
            pdf.multi_cell(0, 6, f"- {safe_f}")
    pdf.ln(4)

    # ── 4. Market Analysis ────────────────────────────────────────
    if market:
        pdf.section_title("4. Local Market Data")
        pdf.key_value("District", market.district)
        pdf.key_value("Population", f"{market.population:,}" if market.population else "N/A")
        pdf.key_value("Road Connectivity", market.road_connectivity)
        pdf.key_value("Nearest Mandi", f"{market.mandi_distance_km} km")
        pdf.key_value("Cold Storage", "Available" if market.cold_storage_available else "Not Available")
        pdf.ln(4)

    # ── 5. Financial Plan ─────────────────────────────────────────
    if fin_plan:
        pdf.section_title("5. Financial Roadmap")
        pdf.key_value("Total Project Cost", f"Rs. {fin_plan.project_cost:,.0f}")
        pdf.key_value("Fixed Cost", f"Rs. {fin_plan.fixed_cost:,.0f}")
        pdf.key_value("Working Capital", f"Rs. {fin_plan.working_capital:,.0f}")
        pdf.key_value("Your Contribution", f"Rs. {fin_plan.user_contribution:,.0f}")
        pdf.key_value("Loan Required", f"Rs. {fin_plan.loan_amount:,.0f}")
        pdf.key_value("Interest Rate", f"{fin_plan.interest_rate}% p.a.")
        pdf.key_value("EMI", f"Rs. {fin_plan.emi:,.0f}")
        pdf.key_value("Repayment Period", f"{fin_plan.repayment_months} months")
        pdf.key_value("Monthly Revenue", f"Rs. {fin_plan.expected_monthly_revenue:,.0f}")
        pdf.key_value("Monthly Expenses", f"Rs. {fin_plan.monthly_expenses:,.0f}")
        pdf.key_value("Net Monthly Profit", f"Rs. {fin_plan.monthly_profit:,.0f}")
        pdf.key_value("Break-even", f"{fin_plan.break_even_months} months")
        pdf.key_value("Annual Income", f"Rs. {fin_plan.annual_income:,.0f}")
        if fin_plan.roi_percentage:
            pdf.key_value("ROI", f"{fin_plan.roi_percentage}%")
        if fin_plan.dscr and fin_plan.dscr < 99:
            pdf.key_value("DSCR", f"{fin_plan.dscr}")
        pdf.ln(4)

    # ── 6. Government Schemes ─────────────────────────────────────
    pdf.section_title("6. Applicable Government Schemes")
    pdf._use_font("", 8)
    pdf.set_text_color(200, 50, 50)
    pdf.cell(0, 5, "(Demo/illustrative scheme records)", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf._use_font("", 10)

    matched_schemes = matched.get("matched_schemes", [])
    if matched_schemes:
        for s in matched_schemes[:5]:
            pdf._use_font("B", 10)
            safe_name = s.name.encode('latin-1', 'replace').decode('latin-1') if not pdf._custom_font else s.name
            pdf.cell(0, 7, safe_name, ln=True)
            pdf._use_font("", 9)
            pdf.key_value("  Type", s.scheme_type)
            pdf.key_value("  Max Support", f"Rs. {s.max_support:,.0f}" if s.max_support else "Varies")
            pdf.key_value("  Support Type", s.support_type or "N/A")
            pdf.ln(2)
    else:
        pdf.cell(0, 7, "No directly matching schemes found.", ln=True)
    pdf.ln(4)

    # ── 7. Recommendations ────────────────────────────────────────
    pdf.section_title("7. Recommended Next Steps")
    steps = [
        "Visit your local Krishi Seva Kendra for detailed guidance.",
        "Prepare a detailed project report (DPR) for loan applications.",
        "Contact the District Industry Centre (DIC) for scheme applications.",
        "Attend skill development training if recommended.",
        "Start with a pilot scale before full investment.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.cell(10)
        pdf.cell(0, 7, f"{i}. {step}", ln=True)

    # ── Output ────────────────────────────────────────────────────
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    filename = f"gramudyam_report_{assessment_id}.pdf"

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
