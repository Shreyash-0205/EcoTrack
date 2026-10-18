# EcoTrack — Smart Waste Management & Segregation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.13](https://img.shields.io/badge/Python-3.13-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask: 3.1](https://img.shields.io/badge/Flask-3.1-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tests: 34 Passed](https://img.shields.io/badge/pytest-34%20passed-brightgreen.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Mapping: Leaflet & OSM](https://img.shields.io/badge/Map-Leaflet%20%2B%20OpenStreetMap-198754.svg?logo=openstreetmap&logoColor=white)](https://leafletjs.com/)
[![UI: Bootstrap 5.3](https://img.shields.io/badge/UI-Bootstrap%205.3-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![University of Mumbai](https://img.shields.io/badge/University%20of%20Mumbai-Sem%20VII%20Mini--Project-blue.svg)](https://mu.ac.in/)

> **EcoTrack** is a full-stack, open-source civic web application designed to empower citizens to report unattended garbage hotspots, scientifically classify waste streams, and track cleanup operations in real time. Built for the **University of Mumbai** Bachelor of Engineering (B.E.) Semester VII curriculum in **Open Source Software Development**.

---

## 1. Project Overview & Societal Impact

Urban centers such as Greater Mumbai generate over 10,000 metric tons of municipal solid waste daily. Mismanaged waste heaps block monsoon stormwater drains, contaminate soil and urban water bodies, and create severe public health hazards. Furthermore, the absence of source segregation forces municipal workers to handle hazardous e-waste and rotting organic waste together.

**EcoTrack solves this by:**
1. Providing a centralized, mobile-responsive portal where citizens can submit hotspot alerts within seconds.
2. Promoting **scientific waste segregation** across 5 discrete streams: **Wet**, **Dry**, **Plastic**, **E-waste**, and **Mixed/Other**.
3. Displaying hotspots on an **interactive Leaflet.js map** powered by **OpenStreetMap**, completely eliminating the need for paid commercial map APIs.
4. Enabling municipal administrators to triage, assign cleanup crews, update statuses (Reported &rarr; In Progress &rarr; Resolved), and log all interventions in an **immutable audit log**.
5. Hardening all inputs through **session CSRF protection**, **salted password hashing (`scrypt`)**, and **Pillow binary image verification**.

---

## 2. Technology Stack (100% Free & Open-Source)

| Component | Technology | Rationale / License |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.13 with Flask 3.1 | Modular, lightweight, highly readable WSGI web framework (BSD-3-Clause). |
| **Database & ORM** | SQLite 3 with SQLAlchemy 2.1 | Zero-configuration, serverless, atomic SQL storage with parameterized queries (MIT/Public Domain). |
| **Geospatial Mapping** | Leaflet.js 1.9 & OpenStreetMap (OSM) | Mobile-friendly mapping engine using open crowd-sourced tile layers (BSD-2-Clause / ODbL). |
| **Data Analytics** | Chart.js 4.4 | Responsive HTML5 canvas charts for waste stream and status funnels (MIT). |
| **Frontend Styling** | HTML5, CSS3, JavaScript, Bootstrap 5.3 | Accessible, clean eco-friendly interface with WCAG 2.1 AA compliant color contrast (MIT). |
| **Automated Testing** | pytest 9.1 with Flask Test Client | 34 automated unit and integration tests executing in isolated test databases (MIT). |
| **Image Security** | Pillow (PIL Fork) 13.0 | Validates image binary integrity to prevent script execution attacks (HPND). |

---

## 3. Core Features

### A. Authentication & Role-Based Access Control (RBAC)
- User registration and login with client and server-side validation.
- Passwords salted and hashed via `werkzeug.security` (`scrypt`).
- Server-side route authorization: `@login_required` and `@admin_required`. Unauthorized administrative access attempts trigger HTTP 403 Forbidden.

### B. Waste Hotspot Reporting
- Report title (5–150 chars), detailed description (10+ chars), landmark, and category.
- **Interactive Leaflet Map Pin-Drop Picker:** Click anywhere on the mini-map to drop or drag a pin to auto-fill latitude and longitude.
- **HTML5 Geolocation:** "Use My Current Location" button acquires GPS coordinates directly from device hardware.
- Optional photographic evidence with client-side preview, 5MB limit, and Pillow binary verification.

### C. Interactive Geospatial Hotspot Map
- Full-screen responsive map of Mumbai and urban areas.
- Status-colored marker pins:
  - <span style="color:#f59e0b; font-weight:bold;">Amber:</span> Reported (Pending)
  - <span style="color:#3b82f6; font-weight:bold;">Blue:</span> In Progress
  - <span style="color:#10b981; font-weight:bold;">Green:</span> Resolved
  - <span style="color:#6b7280; font-weight:bold;">Gray:</span> Rejected
- Clickable popups with thumbnail photos, category badges, landmark info, and direct links to report details.
- Real-time client-side filter controls for waste stream and status.
- Graceful handling of reports without coordinates (clearly counted and tracked via address tables).

### D. Educational Waste Segregation Guide
- Dedicated educational resource detailing Wet (Green Bin), Dry (Blue Bin), Plastic, E-waste, and Mixed/Hazardous waste.
- "What Goes In" vs. "What Must NOT Go In", plus practical everyday eco-tips.
- **Municipal Adaptability Disclaimer:** Explains adaptability to local municipal guidelines (e.g., MCGM Greater Mumbai Bye-Laws and Swachh Bharat rules).

### E. Administrator Management Console & Audit Trail
- System-wide metric counters and Chart.js funnel charts.
- Multi-criteria report management table with search by title, landmark, or citizen name.
- Status transition workflow (Reported &rarr; In Progress &rarr; Resolved / Rejected) with administrator field notes.
- Inappropriate or duplicate report deletion with confirmation safeguards.
- **Immutable Audit Log:** Records every status update, field note modification, and deletion with administrative timestamp and admin ID.

---

## 4. Quick Start & Installation Guide

### Prerequisites
- Python 3.11+ (Python 3.13 recommended)
- Git

### Step-by-Step Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/ecotrack.git
   cd ecotrack
   ```

2. **Create and Activate a Virtual Environment:**
   ```powershell
   # Windows PowerShell:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   ```bash
   # Linux / macOS:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and Seed the Database:**
   ```bash
   python seed_data.py
   ```
   *This initializes `ecotrack.db` with demo accounts and 10 realistic Mumbai metropolitan civic reports (Dadar, Bandra, Juhu, Vashi, Andheri, Marine Drive, Mulund).*

5. **Start the Application Server:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 5. Demonstration Accounts & Local Initialization

EcoTrack includes a local database seeding utility (`seed_data.py`) to set up initial administrative and citizen accounts for evaluation and local testing.

### Local Seeding Command

To initialize the local SQLite database with pre-configured demonstration accounts and sample civic reports, run:

```bash
python seed_data.py
```

Upon successful execution, the script initializes the database tables, generates salted `scrypt` password hashes, and outputs the local initialization status directly to your terminal console:

```text
[EcoTrack Seed] Initializing database tables...
[EcoTrack Seed] Creating demo users...
[EcoTrack Seed] Creating realistic Mumbai civic demo reports...
[EcoTrack Seed] Generating realistic administrative activity logs...
[EcoTrack Seed] Database seeded successfully!
```

### Pre-Configured Demonstration Roles

The seed script initializes the following role-based accounts:

| Role | Name | Email Address | Access & Permissions |
| :--- | :--- | :--- | :--- |
| **Administrator** | Civic Administrator (MCGM) | `admin@ecotrack.org` | Full access to Admin Dashboard (`/admin/dashboard`), Status Triage (`/admin/manage-reports`), Report Deletion, and System Audit Logs (`/admin/logs`). |
| **Citizen** | Aarav Sharma | `citizen@ecotrack.org` | Citizen Dashboard (`/dashboard`), Hotspot Reporting (`/report`), and editing pending complaints (`/my-reports`). |
| **Citizen** | Priya Deshmukh | `priya@ecotrack.org` | Citizen Dashboard (`/dashboard`), Hotspot Reporting (`/report`), and personal complaint tracking. |
| **Citizen** | Rohan Kulkarni | `rohan@ecotrack.org` | Citizen Dashboard (`/dashboard`), Hotspot Reporting (`/report`), and personal complaint tracking. |

> **Note on Local Passwords:** To avoid exposing hardcoded credentials in published source code, `seed_data.py` reads initial demonstration passwords from environment variables (`ECOTRACK_ADMIN_PASSWORD` and `ECOTRACK_CITIZEN_PASSWORD`) or generates secure random passwords during local database initialization, outputting them directly to your local terminal.

### Registering New Accounts

You can also create fresh citizen accounts at any time through the application interface:
1. Navigate to `http://127.0.0.1:5000/auth/register` (or click **Register** in the navigation bar).
2. Complete the registration form with your name, email, and password.
3. Sign in immediately at `http://127.0.0.1:5000/auth/login`.

---

## 6. Automated Testing

EcoTrack comes with a complete automated test suite verifying authentication, authorization, reporting, form validation, safe image uploads, and database constraints.

To execute the test suite:
```bash
pytest
```

**Test Execution Output:**
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1
rootdir: C:\Users\Shreyash\SEM 7\EcoTrack
configfile: pytest.ini
testpaths: tests
collected 34 items

tests\test_admin.py ......                                               [ 17%]
tests\test_auth.py .........                                             [ 44%]
tests\test_database.py ....                                              [ 55%]
tests\test_reports.py .......                                            [ 76%]
tests\test_validation_and_security.py ........                           [100%]

============================= 34 passed in 19.68s =============================
```

---

## 7. Project Architecture & Directory Layout

```text
EcoTrack/
├── app.py                     # Flask application factory, error handlers & context processors
├── config.py                  # Configurations (Development, Testing, Production)
├── requirements.txt           # Python dependency specifications
├── pytest.ini                 # Pytest configuration and path settings
├── seed_data.py               # Realistic Mumbai civic seed dataset generator
├── LICENSE                    # MIT Open-Source License
├── README.md                  # Comprehensive project documentation
├── CONTRIBUTING.md            # Contribution guidelines & upstream project suggestions
├── CODE_OF_CONDUCT.md         # Contributor Covenant Code of Conduct (v2.1)
├── SECURITY.md                # Security policy & vulnerability reporting instructions
├── ROADMAP.md                 # Documented milestones (v1.0 to v2.0)
├── .gitignore                 # Git ignore rules for virtualenvs, caches, and databases
├── .github/                   # GitHub community health templates
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── models/                    # SQLAlchemy database models
│   ├── __init__.py
│   ├── user.py                # User model with scrypt hashing and role checks
│   ├── report.py              # Report model with categories, coordinates, and status
│   └── activity_log.py        # Audit log model for administrative interventions
├── routes/                    # Modular Flask blueprints
│   ├── __init__.py
│   ├── auth.py                # Registration, login, logout, and session handling
│   ├── main.py                # Landing page, guide, map view, about
│   ├── citizen.py             # Hotspot submission, personal dashboard, editing
│   ├── admin.py               # Admin dashboard, status triage, deletion, audit logs
│   └── api.py                 # REST endpoints for Leaflet map & safe image delivery
├── static/                    # Frontend static assets
│   ├── css/
│   │   └── style.css          # Eco-friendly theme, custom badges, marker pins
│   └── js/
│       ├── main.js            # Alerts, client-side validation, image preview, geolocation
│       ├── map.js             # Leaflet OpenStreetMap logic, filters, and coordinate picker
│       └── charts.js          # Chart.js category doughnut and status funnel charts
├── templates/                 # Semantic Jinja2 HTML5 templates
│   ├── base.html              # Master layout with CDNs, navbar, alerts, footer
│   ├── navbar.html            # Responsive navigation bar with role-based links
│   ├── footer.html            # Academic attribution and quick links
│   ├── pages/                 # Public pages (index, guide, map_view, about)
│   ├── auth/                  # Authentication pages (login, register)
│   ├── citizen/               # Citizen views (dashboard, report_waste, my_reports, detail, edit)
│   ├── admin/                 # Administrator views (dashboard, manage_reports, logs)
│   └── errors/                # Safe error pages (400, 403, 404, 500)
├── uploads/                   # Physical uploaded image directory
│   └── reports/
│       └── .gitkeep
├── tests/                     # Automated pytest suite
│   ├── conftest.py            # Test app fixtures, in-memory DB, sample users, dummy images
│   ├── test_auth.py           # Registration, login, duplicate email, password strength
│   ├── test_reports.py        # Report CRUD, coordinates handling, photo uploads
│   ├── test_admin.py          # Admin authorization, status updates, deletion, audit trail
│   ├── test_validation_and_security.py # Category whitelist, coordinate bounds, path traversal
│   └── test_database.py       # Model methods, foreign key cascades, coordinate logic
└── docs/                      # University of Mumbai academic submission documentation
    ├── 01_problem_statement.md
    ├── 02_abstract.md
    ├── 03_objectives_and_scope.md
    ├── 04_existing_vs_proposed_system.md
    ├── 05_literature_and_repository_survey.md
    ├── 06_functional_and_nonfunctional_requirements.md
    ├── 07_system_architecture.md
    ├── 08_use_case_diagram.md
    ├── 09_data_flow_diagrams.md
    ├── 10_er_diagram_and_schema.md
    ├── 11_weekly_gantt_chart.md
    ├── 12_weekly_group_logbook.md
    ├── 13_test_cases_and_validation_results.md
    ├── 14_limitations_and_future_scope.md
    ├── 15_conclusion_and_references.md
    ├── team_contribution_matrix.md
    └── university_mini_project_report_template.md
```

---

## 8. University of Mumbai Mini-Project Documentation

For academic evaluation under the University of Mumbai Bachelor of Engineering curriculum, refer to the editable documentation suite in the [`docs/`](docs/) directory:
- [Problem Statement](docs/01_problem_statement.md)
- [Abstract](docs/02_abstract.md)
- [Objectives & Scope](docs/03_objectives_and_scope.md)
- [Existing vs. Proposed System](docs/04_existing_vs_proposed_system.md)
- [Literature & Open-Source Repository Survey](docs/05_literature_and_repository_survey.md)
- [Functional & Non-Functional Requirements](docs/06_functional_and_nonfunctional_requirements.md)
- [System Architecture](docs/07_system_architecture.md)
- [Use-Case Diagram & Specifications](docs/08_use_case_diagram.md)
- [Data-Flow Diagrams (Level 0 & Level 1)](docs/09_data_flow_diagrams.md)
- [ER Diagram & Relational Schema](docs/10_er_diagram_and_schema.md)
- [8-Week Implementation Gantt Chart](docs/11_weekly_gantt_chart.md)
- [8-Week Weekly Group Logbook](docs/12_weekly_group_logbook.md)
- [Test Cases & Validation Results Matrix (34 Tests)](docs/13_test_cases_and_validation_results.md)
- [Limitations & Future Scope](docs/14_limitations_and_future_scope.md)
- [Conclusion & References](docs/15_conclusion_and_references.md)
- [Student Contribution Matrix (4 or 3 Students)](docs/team_contribution_matrix.md)
- [Formal University Project Report Template](docs/university_mini_project_report_template.md)

---

## 9. License

This project is open-source software licensed under the terms of the [MIT License](LICENSE). Third-party libraries (Flask, Bootstrap, Leaflet, Chart.js, Pillow, pytest) are used in accordance with their respective open-source licenses.

