"""
GramUdyam AI – Seed Data
==========================

Realistic demo data for 3 Maharashtra districts.
All financial figures are in INR (₹).
"""

from app.database import SessionLocal, engine
from app.models import (
    Base, User, BusinessOpportunity, LocalMarketData, GovernmentScheme
)


def seed_database():
    """Create tables and seed with demo data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Skip if data exists
        if db.query(User).first():
            print("Database already seeded.")
            return

        # ── Demo Users ────────────────────────────────────────────────
        users = [
            User(username="demo_farmer", full_name="Demo Farmer", role="farmer", language="en"),
            User(username="demo_officer", full_name="District Officer", role="officer", language="en"),
            User(username="demo_admin", full_name="System Admin", role="admin", language="en"),
        ]
        db.add_all(users)
        db.flush()

        # ── Business Opportunities ────────────────────────────────────
        businesses = [
            BusinessOpportunity(
                name="Dairy Farming",
                name_hi="डेयरी फार्मिंग",
                name_mr="दुग्ध व्यवसाय",
                category="dairy",
                description="Milk production and sale with 3-5 cows/buffaloes. Includes fresh milk sale and value-added products.",
                description_hi="3-5 गायों/भैंसों के साथ दूध उत्पादन और बिक्री।",
                description_mr="3-5 गायी/म्हशींसह दूध उत्पादन आणि विक्री.",
                required_investment_min=80000,
                required_investment_max=200000,
                expected_monthly_revenue=30000,
                estimated_monthly_cost=18000,
                estimated_monthly_profit=12000,
                break_even_months=14,
                required_land=0.5,
                required_skills="animal husbandry,cattle care,basic accounting",
                risk_level="Medium",
                seasonality_factor=0.85,
                infrastructure_requirement="Medium",
                local_demand_base=0.80,
                competition_base=0.55,
            ),
            BusinessOpportunity(
                name="Goat Farming",
                name_hi="बकरी पालन",
                name_mr="शेळीपालन",
                category="livestock",
                description="Commercial goat rearing for meat and milk. Low investment, high demand business.",
                description_hi="मांस और दूध के लिए व्यावसायिक बकरी पालन।",
                description_mr="मांस आणि दुधासाठी व्यावसायिक शेळीपालन.",
                required_investment_min=50000,
                required_investment_max=150000,
                expected_monthly_revenue=25000,
                estimated_monthly_cost=12000,
                estimated_monthly_profit=13000,
                break_even_months=10,
                required_land=0.25,
                required_skills="animal care,grazing management",
                risk_level="Low",
                seasonality_factor=0.75,
                infrastructure_requirement="Low",
                local_demand_base=0.75,
                competition_base=0.40,
            ),
            BusinessOpportunity(
                name="Vermicomposting",
                name_hi="वर्मीकम्पोस्ट",
                name_mr="गांडूळ खत निर्मिती",
                category="organic",
                description="Organic manure production using earthworms. Growing demand from organic farmers.",
                description_hi="केंचुओं का उपयोग करके जैविक खाद उत्पादन।",
                description_mr="गांडुळांचा वापर करून सेंद्रिय खत उत्पादन.",
                required_investment_min=20000,
                required_investment_max=80000,
                expected_monthly_revenue=18000,
                estimated_monthly_cost=6000,
                estimated_monthly_profit=12000,
                break_even_months=6,
                required_land=0.1,
                required_skills="composting,agriculture,organic farming",
                risk_level="Low",
                seasonality_factor=0.90,
                infrastructure_requirement="Low",
                local_demand_base=0.65,
                competition_base=0.30,
            ),
            BusinessOpportunity(
                name="Food Processing Unit",
                name_hi="खाद्य प्रसंस्करण इकाई",
                name_mr="अन्न प्रक्रिया युनिट",
                category="food_processing",
                description="Processing pickles, papad, spices, and snacks. Value addition to local agricultural produce.",
                description_hi="अचार, पापड, मसाले और स्नैक्स की प्रसंस्करण इकाई।",
                description_mr="लोणचे, पापड, मसाले आणि स्नॅक्स प्रक्रिया युनिट.",
                required_investment_min=100000,
                required_investment_max=300000,
                expected_monthly_revenue=45000,
                estimated_monthly_cost=28000,
                estimated_monthly_profit=17000,
                break_even_months=16,
                required_land=0.15,
                required_skills="food processing,hygiene,packaging,marketing",
                risk_level="Medium",
                seasonality_factor=0.70,
                infrastructure_requirement="Medium",
                local_demand_base=0.70,
                competition_base=0.50,
            ),
            BusinessOpportunity(
                name="Poultry Farming",
                name_hi="मुर्गीपालन",
                name_mr="कुक्कुटपालन",
                category="poultry",
                description="Broiler or layer poultry farming with 200-500 birds. Quick returns.",
                description_hi="200-500 मुर्गियों के साथ ब्रॉयलर या लेयर मुर्गीपालन।",
                description_mr="200-500 पक्ष्यांसह ब्रॉयलर किंवा लेयर कुक्कुटपालन.",
                required_investment_min=60000,
                required_investment_max=200000,
                expected_monthly_revenue=35000,
                estimated_monthly_cost=22000,
                estimated_monthly_profit=13000,
                break_even_months=12,
                required_land=0.2,
                required_skills="poultry management,disease prevention",
                risk_level="Medium",
                seasonality_factor=0.80,
                infrastructure_requirement="Medium",
                local_demand_base=0.85,
                competition_base=0.60,
            ),
            BusinessOpportunity(
                name="Beekeeping",
                name_hi="मधुमक्खी पालन",
                name_mr="मधमाशी पालन",
                category="beekeeping",
                description="Honey production and pollination services. Low maintenance, eco-friendly business.",
                description_hi="शहद उत्पादन और परागण सेवाएं।",
                description_mr="मध उत्पादन आणि परागीकरण सेवा.",
                required_investment_min=25000,
                required_investment_max=80000,
                expected_monthly_revenue=15000,
                estimated_monthly_cost=5000,
                estimated_monthly_profit=10000,
                break_even_months=7,
                required_land=0.05,
                required_skills="beekeeping,agriculture",
                risk_level="Low",
                seasonality_factor=0.60,
                infrastructure_requirement="Low",
                local_demand_base=0.55,
                competition_base=0.25,
            ),
            BusinessOpportunity(
                name="Agri-Input Store",
                name_hi="कृषि इनपुट दुकान",
                name_mr="कृषी निविष्ठा दुकान",
                category="retail",
                description="Retail shop for seeds, fertilizers, pesticides, and farm tools.",
                description_hi="बीज, उर्वरक, कीटनाशक और कृषि उपकरणों की खुदरा दुकान।",
                description_mr="बियाणे, खते, कीटकनाशके आणि शेती अवजारांचे किरकोळ दुकान.",
                required_investment_min=150000,
                required_investment_max=400000,
                expected_monthly_revenue=60000,
                estimated_monthly_cost=45000,
                estimated_monthly_profit=15000,
                break_even_months=22,
                required_land=0.02,
                required_skills="retail,agriculture knowledge,accounting,marketing",
                risk_level="Medium",
                seasonality_factor=0.65,
                infrastructure_requirement="Medium",
                local_demand_base=0.75,
                competition_base=0.55,
            ),
            BusinessOpportunity(
                name="Vegetable Processing",
                name_hi="सब्जी प्रसंस्करण",
                name_mr="भाजीपाला प्रक्रिया",
                category="food_processing",
                description="Dehydration, grading, and packaging of vegetables for urban markets.",
                description_hi="शहरी बाजारों के लिए सब्जियों का निर्जलीकरण, ग्रेडिंग और पैकेजिंग।",
                description_mr="शहरी बाजारपेठांसाठी भाजीपाला निर्जलीकरण, प्रतवारी आणि पॅकेजिंग.",
                required_investment_min=80000,
                required_investment_max=250000,
                expected_monthly_revenue=40000,
                estimated_monthly_cost=25000,
                estimated_monthly_profit=15000,
                break_even_months=14,
                required_land=0.1,
                required_skills="food processing,grading,packaging,supply chain",
                risk_level="Medium",
                seasonality_factor=0.65,
                infrastructure_requirement="High",
                local_demand_base=0.60,
                competition_base=0.45,
            ),
        ]
        db.add_all(businesses)
        db.flush()

        # ── Local Market Data (3 Maharashtra districts) ───────────────
        market_data = [
            LocalMarketData(
                district="Ahmednagar",
                state="Maharashtra",
                population=4543159,
                num_villages=1530,
                existing_businesses={
                    "dairy": 320, "livestock": 180, "organic": 45,
                    "food_processing": 90, "poultry": 210, "beekeeping": 35,
                    "retail": 560, "agri_services": 120
                },
                competitor_density={
                    "dairy": 0.55, "livestock": 0.35, "organic": 0.20,
                    "food_processing": 0.40, "poultry": 0.50, "beekeeping": 0.15,
                    "retail": 0.65, "agri_services": 0.30
                },
                market_prices={
                    "milk_per_litre": 32, "goat_per_kg": 650,
                    "vermicompost_per_kg": 8, "eggs_per_dozen": 65,
                    "honey_per_kg": 350, "wheat_per_quintal": 2200,
                    "onion_per_quintal": 1500, "soybean_per_quintal": 4200,
                    "tomato_per_kg": 25, "potato_per_kg": 20
                },
                seasonal_demand={
                    "Jan": 0.7, "Feb": 0.7, "Mar": 0.8, "Apr": 0.9,
                    "May": 1.0, "Jun": 0.8, "Jul": 0.6, "Aug": 0.6,
                    "Sep": 0.7, "Oct": 0.9, "Nov": 1.0, "Dec": 0.8
                },
                nearby_towns=[
                    {"name": "Ahmednagar City", "distance_km": 0, "population": 350000},
                    {"name": "Sangamner", "distance_km": 50, "population": 65000},
                    {"name": "Shrirampur", "distance_km": 35, "population": 70000},
                    {"name": "Rahuri", "distance_km": 30, "population": 45000},
                ],
                road_connectivity="Good",
                internet_connectivity="Medium",
                banking_access="Good",
                electricity_reliability="Good",
                cold_storage_available=True,
                mandi_distance_km=15,
            ),
            LocalMarketData(
                district="Pune",
                state="Maharashtra",
                population=9429408,
                num_villages=1866,
                existing_businesses={
                    "dairy": 480, "livestock": 220, "organic": 120,
                    "food_processing": 350, "poultry": 280, "beekeeping": 55,
                    "retail": 890, "agri_services": 210
                },
                competitor_density={
                    "dairy": 0.65, "livestock": 0.40, "organic": 0.35,
                    "food_processing": 0.55, "poultry": 0.55, "beekeeping": 0.20,
                    "retail": 0.75, "agri_services": 0.45
                },
                market_prices={
                    "milk_per_litre": 35, "goat_per_kg": 700,
                    "vermicompost_per_kg": 10, "eggs_per_dozen": 70,
                    "honey_per_kg": 400, "wheat_per_quintal": 2300,
                    "onion_per_quintal": 1600, "soybean_per_quintal": 4400,
                    "tomato_per_kg": 30, "potato_per_kg": 22
                },
                seasonal_demand={
                    "Jan": 0.8, "Feb": 0.8, "Mar": 0.9, "Apr": 0.9,
                    "May": 1.0, "Jun": 0.7, "Jul": 0.6, "Aug": 0.7,
                    "Sep": 0.8, "Oct": 0.9, "Nov": 1.0, "Dec": 0.9
                },
                nearby_towns=[
                    {"name": "Pune City", "distance_km": 0, "population": 3100000},
                    {"name": "Baramati", "distance_km": 100, "population": 65000},
                    {"name": "Junnar", "distance_km": 95, "population": 40000},
                    {"name": "Shirur", "distance_km": 70, "population": 50000},
                ],
                road_connectivity="Good",
                internet_connectivity="Good",
                banking_access="Good",
                electricity_reliability="Good",
                cold_storage_available=True,
                mandi_distance_km=10,
            ),
            LocalMarketData(
                district="Nashik",
                state="Maharashtra",
                population=6107187,
                num_villages=1933,
                existing_businesses={
                    "dairy": 290, "livestock": 160, "organic": 70,
                    "food_processing": 180, "poultry": 190, "beekeeping": 60,
                    "retail": 450, "agri_services": 130
                },
                competitor_density={
                    "dairy": 0.50, "livestock": 0.30, "organic": 0.25,
                    "food_processing": 0.45, "poultry": 0.45, "beekeeping": 0.18,
                    "retail": 0.60, "agri_services": 0.28
                },
                market_prices={
                    "milk_per_litre": 33, "goat_per_kg": 680,
                    "vermicompost_per_kg": 9, "eggs_per_dozen": 62,
                    "honey_per_kg": 380, "wheat_per_quintal": 2250,
                    "onion_per_quintal": 1800, "soybean_per_quintal": 4300,
                    "grape_per_kg": 60, "tomato_per_kg": 22
                },
                seasonal_demand={
                    "Jan": 0.8, "Feb": 0.9, "Mar": 0.9, "Apr": 0.8,
                    "May": 0.9, "Jun": 0.7, "Jul": 0.5, "Aug": 0.6,
                    "Sep": 0.7, "Oct": 0.9, "Nov": 1.0, "Dec": 0.9
                },
                nearby_towns=[
                    {"name": "Nashik City", "distance_km": 0, "population": 1500000},
                    {"name": "Malegaon", "distance_km": 120, "population": 470000},
                    {"name": "Sinnar", "distance_km": 30, "population": 40000},
                    {"name": "Igatpuri", "distance_km": 45, "population": 30000},
                ],
                road_connectivity="Good",
                internet_connectivity="Medium",
                banking_access="Good",
                electricity_reliability="Medium",
                cold_storage_available=True,
                mandi_distance_km=12,
            ),
        ]
        db.add_all(market_data)
        db.flush()

        # ── Government Schemes ────────────────────────────────────────
        schemes = [
            GovernmentScheme(
                name="Pradhan Mantri Mudra Yojana (PMMY)",
                name_hi="प्रधानमंत्री मुद्रा योजना",
                name_mr="प्रधानमंत्री मुद्रा योजना",
                scheme_type="Central",
                department="Ministry of Finance",
                eligible_categories=["all", "dairy", "food_processing", "retail", "livestock", "poultry"],
                max_support=1000000,
                support_type="Loan",
                subsidy_percentage=0,
                eligibility_criteria="Any Indian citizen with a business plan for a non-farm income generating activity.",
                required_documents=["Aadhaar Card", "PAN Card", "Business Plan", "Address Proof", "Caste Certificate (if SC/ST/OBC)"],
                description="Collateral-free loans up to ₹10 lakh for micro & small enterprises under Shishu (up to ₹50K), Kishore (₹50K–5L), and Tarun (₹5L–10L) categories.",
                description_hi="सूक्ष्म और लघु उद्यमों के लिए ₹10 लाख तक के बिना गारंटी ऋण।",
                description_mr="सूक्ष्म आणि लघु उद्योगांसाठी ₹10 लाखांपर्यंत बिनातारण कर्ज.",
            ),
            GovernmentScheme(
                name="National Livestock Mission (NLM)",
                name_hi="राष्ट्रीय पशुधन मिशन",
                name_mr="राष्ट्रीय पशुधन अभियान",
                scheme_type="Central",
                department="Department of Animal Husbandry",
                eligible_categories=["dairy", "livestock", "poultry", "beekeeping"],
                max_support=500000,
                support_type="Subsidy",
                subsidy_percentage=50,
                eligibility_criteria="Farmers and entrepreneurs interested in livestock-based livelihoods.",
                required_documents=["Aadhaar Card", "Land Document", "Bank Passbook", "Caste Certificate", "Project Report"],
                description="Up to 50% subsidy on livestock-related projects for breed improvement, feed, and infrastructure.",
                description_hi="पशुधन परियोजनाओं पर 50% तक की सब्सिडी।",
                description_mr="पशुधन प्रकल्पांवर 50% पर्यंत अनुदान.",
            ),
            GovernmentScheme(
                name="PM Kisan Sampada Yojana",
                name_hi="प्रधानमंत्री किसान संपदा योजना",
                name_mr="प्रधानमंत्री किसान संपदा योजना",
                scheme_type="Central",
                department="Ministry of Food Processing Industries",
                eligible_categories=["food_processing", "organic"],
                max_support=500000,
                support_type="Grant",
                subsidy_percentage=35,
                eligibility_criteria="Groups, cooperatives, or entrepreneurs establishing food processing units.",
                required_documents=["Aadhaar Card", "PAN Card", "DPR (Detailed Project Report)", "Land/Lease Document", "FSSAI License (or application)"],
                description="35% grant-in-aid for food processing infrastructure, cold chains, and value addition.",
                description_hi="खाद्य प्रसंस्करण अवसंरचना के लिए 35% अनुदान।",
                description_mr="अन्न प्रक्रिया पायाभूत सुविधांसाठी 35% अनुदान.",
            ),
            GovernmentScheme(
                name="Maharashtra State Rural Livelihoods Mission (MSRLM)",
                name_hi="महाराष्ट्र राज्य ग्रामीण आजीविका मिशन",
                name_mr="महाराष्ट्र राज्य ग्रामीण उपजीविका अभियान",
                scheme_type="State",
                department="Maharashtra Rural Development Department",
                eligible_categories=["all", "dairy", "livestock", "food_processing", "organic"],
                max_support=300000,
                support_type="Loan + Subsidy",
                subsidy_percentage=30,
                eligibility_criteria="Rural women SHG members and BPL families in Maharashtra.",
                required_documents=["Aadhaar Card", "BPL Card", "SHG Membership", "Bank Account Details"],
                description="Financial and technical support for SHGs and rural entrepreneurs through revolving fund and community investment.",
                description_hi="स्वयं सहायता समूहों के लिए वित्तीय और तकनीकी सहायता।",
                description_mr="बचत गटांसाठी आर्थिक आणि तांत्रिक सहाय्य.",
            ),
            GovernmentScheme(
                name="Rashtriya Krishi Vikas Yojana (RKVY)",
                name_hi="राष्ट्रीय कृषि विकास योजना",
                name_mr="राष्ट्रीय कृषी विकास योजना",
                scheme_type="Central",
                department="Department of Agriculture & Cooperation",
                eligible_categories=["agriculture", "organic", "dairy", "food_processing"],
                max_support=250000,
                support_type="Subsidy",
                subsidy_percentage=50,
                eligibility_criteria="Farmers, FPOs, and agri-entrepreneurs with valid agriculture projects.",
                required_documents=["Aadhaar Card", "Land Records (7/12 Extract)", "Project Proposal", "Bank Account"],
                description="Financial support for agricultural diversification, mechanization, and value chain development.",
                description_hi="कृषि विविधीकरण के लिए वित्तीय सहायता।",
                description_mr="कृषी विविधीकरणासाठी आर्थिक सहाय्य.",
            ),
            GovernmentScheme(
                name="National Beekeeping & Honey Mission (NBHM)",
                name_hi="राष्ट्रीय मधुमक्खी पालन एवं शहद मिशन",
                name_mr="राष्ट्रीय मधमाशी पालन आणि मध अभियान",
                scheme_type="Central",
                department="National Bee Board, KVIC",
                eligible_categories=["beekeeping"],
                max_support=200000,
                support_type="Subsidy",
                subsidy_percentage=65,
                eligibility_criteria="Individuals, SHGs, and FPOs interested in beekeeping.",
                required_documents=["Aadhaar Card", "Bank Account", "Training Certificate (if any)", "Land Proof"],
                description="Up to 65% subsidy on beekeeping setup, bee colonies, and honey processing equipment.",
                description_hi="मधुमक्खी पालन सेटअप पर 65% तक की सब्सिडी।",
                description_mr="मधमाशी पालन सेटअपवर 65% पर्यंत अनुदान.",
            ),
            GovernmentScheme(
                name="Magel Tyala Sheli/Mendhi Yojana",
                name_hi="मागेल त्याला शेळी/मेंढी योजना",
                name_mr="मागेल त्याला शेळी/मेंढी योजना",
                scheme_type="State",
                department="Maharashtra Animal Husbandry Department",
                eligible_categories=["livestock"],
                max_support=400000,
                support_type="Subsidy",
                subsidy_percentage=75,
                eligibility_criteria="SC/ST/OBC farmers in Maharashtra interested in goat/sheep farming.",
                required_documents=["Aadhaar Card", "Caste Certificate", "Land Proof", "Bank Account", "7/12 Extract"],
                description="75% subsidy for 10+1 goat unit (SC/ST) or 50% subsidy for general category farmers.",
                description_hi="बकरी इकाई पर 75% सब्सिडी (अनुसूचित जाति/जनजाति)।",
                description_mr="शेळी/मेंढी युनिटवर 75% अनुदान (अनुसूचित जाती/जमाती).",
            ),
            GovernmentScheme(
                name="PMEGP (Prime Minister's Employment Generation Programme)",
                name_hi="प्रधानमंत्री रोजगार सृजन कार्यक्रम",
                name_mr="प्रधानमंत्री रोजगार निर्मिती कार्यक्रम",
                scheme_type="Central",
                department="Ministry of MSME / KVIC",
                eligible_categories=["all", "food_processing", "retail", "organic"],
                max_support=2500000,
                support_type="Subsidy",
                subsidy_percentage=35,
                eligibility_criteria="Individuals above 18 years. For manufacturing: project up to ₹50 lakh; for services: up to ₹20 lakh.",
                required_documents=["Aadhaar Card", "PAN Card", "Educational Certificate", "Detailed Project Report", "EDP Training Certificate"],
                description="15-35% subsidy on project cost. Higher subsidy for SC/ST/Women/Minorities in rural areas.",
                description_hi="परियोजना लागत पर 15-35% सब्सिडी।",
                description_mr="प्रकल्प खर्चावर 15-35% अनुदान.",
            ),
        ]
        db.add_all(schemes)

        db.commit()
        print("Database seeded successfully with demo data.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
