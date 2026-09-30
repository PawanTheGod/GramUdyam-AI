# 🌾 GramUdyam AI (ग्रामउद्यम AI)

> **AI-Powered Local Business Discovery, Feasibility & Financial Advisory for Rural Entrepreneurs & Farmers**

GramUdyam AI is a full-stack platform designed to empower rural entrepreneurs, farmers, and self-help groups (SHGs) with data-driven business discovery, AI feasibility scoring, financial planning, government scheme matching, and multilingual accessibility (English, Marathi, and Hindi).

---

## 🌟 Key Features

1. **🌾 Multilingual Discovery & Advisory**: Full tri-lingual interface (English, मराठी, हिंदी) tailored for rural users and district administrators.
2. **📊 Business Discovery Engine**: Searchable rural business catalogue (Dairy, Poultry, Agro-processing, Organic Farming, Cold Storage, etc.) with estimated investment ranges, operational requirements, and profitability insights.
3. **⚡ AI-Assisted Feasibility Assessment**: Multi-dimensional scoring across:
   - Resource Availability (Land, Water, Power, Logistics)
   - Market Demand & District Readiness
   - Financial Viability & ROI Projections
   - Risk & Mitigation Strategies
4. **💰 Dynamic Financial Roadmap & Loan Calculator**:
   - CapEx vs. OpEx breakdown
   - EMI calculation with tenure and interest sliders
   - Break-even & Payback period estimation
   - Cash flow projections
5. **🏛️ Government Scheme Intelligence**: Automated rule-based matching for central & state schemes (PMEGP, PMFME, AIF, Mudra, NABARD, Stand-Up India).
6. **📄 Exportable Business Feasibility Reports**: Download structured feasibility summaries for bank loan applications.
7. **👥 Role-Based Authentication & Profiles**: Farmer / Entrepreneur and Admin roles with pre-configured demo logins.

---

## 🏗️ Architecture & Tech Stack

```
gramUdyog/
├── backend/                  # FastAPI Python Backend
│   ├── app/
│   │   ├── main.py           # Application entry & router setup
│   │   ├── database.py       # SQLAlchemy SQLite / PostgreSQL setup
│   │   ├── models.py         # ORM models (User, Profile, Assessment, etc.)
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── seed_data.py      # Pre-seeded rural business data & schemes
│   │   └── routers/          # Modular API endpoints
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React + Vite + TypeScript Frontend
│   ├── src/
│   │   ├── api/              # Axios API client
│   │   ├── components/       # UI layout, charts, navigation
│   │   ├── contexts/         # Auth and Language Contexts
│   │   ├── i18n/             # Translations (en, mr, hi)
│   │   ├── pages/            # Dashboard, Discovery, Feasibility, Financial, etc.
│   │   └── App.tsx           # Routes & Application Root
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

### Technology Highlights
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons, Recharts
- **Backend**: FastAPI, Python 3.10+, SQLAlchemy, Pydantic, SQLite (PostgreSQL compatible)
- **Security & Auth**: JWT-based Bearer authentication, Password hashing (passlib/bcrypt)

---

## 🚀 Getting Started

### 1. Prerequisites
- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://www.python.org/) (v3.10+)
- [Git](https://git-scm.com/)

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn app.main:app --reload --port 8000
```
Backend API Docs will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Access the application at: [http://localhost:5173](http://localhost:5173)

---

## 🔑 Demo Credentials

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Farmer / Entrepreneur** | `ramesh_farmer` | `demo123` | Feasibility analysis, financial roadmap & scheme matching |
| **District Admin** | `admin_officer` | `demo123` | Aggregate district dashboard, business trends & approvals |

---

## 📜 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
