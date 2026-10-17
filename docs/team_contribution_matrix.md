# Team Contribution Matrix & Role Allocations

This document defines the formal division of engineering responsibilities for the University of Mumbai Bachelor of Engineering Semester VII Open Source Software Development mini-project.

---

## 1. Team Allocation for Four (4) Students

| Team Member | Academic Role | Primary Responsibilities | Concrete Code & Document Deliverables |
| :--- | :--- | :--- | :--- |
| **Student 1**<br>Name: `[Insert Student 1 Name]`<br>Roll No: `[Insert Roll No]` | **Backend Architecture & Database Engineering** | - Flask application factory setup (`app.py`, `config.py`)<br>- SQLAlchemy ORM models (`models/user.py`, `models/report.py`, `models/activity_log.py`)<br>- Password hashing & session state management<br>- Relational schema constraints, indexing, and foreign key cascades | - `app.py`<br>- `config.py`<br>- `models/__init__.py`, `user.py`, `report.py`, `activity_log.py`<br>- `routes/auth.py`<br>- `seed_data.py` (database seeding) |
| **Student 2**<br>Name: `[Insert Student 2 Name]`<br>Roll No: `[Insert Roll No]` | **Frontend UI/UX & Digital Accessibility** | - Semantic HTML5 responsive templates (`templates/`)<br>- Custom eco stylesheet (`static/css/style.css`)<br>- WCAG 2.1 AA compliant color contrast & accessibility design<br>- Waste Segregation Guide educational page<br>- Client-side forms, modals, and file size checks (`main.js`) | - `templates/base.html`, `navbar.html`, `footer.html`<br>- `templates/pages/index.html`, `segregation_guide.html`<br>- `templates/citizen/report_waste.html`, `my_reports.html`<br>- `static/css/style.css`<br>- `static/js/main.js` |
| **Student 3**<br>Name: `[Insert Student 3 Name]`<br>Roll No: `[Insert Roll No]` | **Quality Assurance, Testing & University Documentation** | - Comprehensive automated test suite with `pytest`<br>- CSRF validation & security hardening (`utils/security.py`)<br>- Safe file upload validation using Pillow binary checks<br>- University documentation suite (15 docs, Gantt, logbook)<br>- Traceability & validation matrix | - `tests/conftest.py`, `test_auth.py`, `test_reports.py`, `test_admin.py`, `test_validation_and_security.py`, `test_database.py`<br>- `utils/security.py`<br>- `pytest.ini`<br>- Complete `docs/` folder suite & university report |
| **Student 4**<br>Name: `[Insert Student 4 Name]`<br>Roll No: `[Insert Roll No]` | **Geospatial Mapping, Analytics & Full-Stack Integration** | - Leaflet.js with OpenStreetMap integration (`static/js/map.js`)<br>- Interactive click-to-pin coordinate picker & HTML5 GPS<br>- REST API endpoints (`/api/reports`, `/api/stats`)<br>- Chart.js analytics for citizen & administrator dashboards<br>- Dynamic multi-criteria filtering on map pins | - `static/js/map.js`<br>- `static/js/charts.js`<br>- `routes/api.py`<br>- `templates/pages/map_view.html`<br>- `templates/admin/dashboard.html`, `manage_reports.html`, `logs.html` |

---

## 2. Adaptation for a Group of Three (3) Students

If the project is executed by a 3-member engineering team, Student 4's duties are consolidated as follows:

| 3-Member Role | Consolidated Responsibilities | Merged Deliverables |
| :--- | :--- | :--- |
| **Member A (Backend, Database & APIs)** | Student 1's backend tasks + Student 4's REST API endpoints (`/api/reports`, `/api/stats`) and database indexing. | `app.py`, `config.py`, `models/`, `routes/auth.py`, `routes/api.py`, `seed_data.py`. |
| **Member B (Frontend, Maps & Analytics)** | Student 2's UI/UX styling + Student 4's Leaflet.js mapping (`map.js`) and Chart.js integration (`charts.js`). | `templates/`, `static/css/style.css`, `static/js/main.js`, `static/js/map.js`, `static/js/charts.js`. |
| **Member C (Security, Testing & Documentation)** | Student 3's full test suite + security filters, Pillow verification, and compilation of Mumbai University project reports. | `tests/`, `utils/security.py`, `docs/`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`. |

---

## 3. Academic Integrity & Verification Guidelines
- **No Fabricated Data:** Survey numbers, faculty approvals, and test results must reflect genuine verified executions.
- **Genuine Open-Source Evidence:** If submitting upstream contributions (e.g., to OpenStreetMap or OpenAQ), students must record their genuine pull request URL, commit SHA hash, and reviewer comments in their lab portfolio.
- **Faculty Review Placeholder:**  
  `Faculty Guide Name: _____________________________________`  
  `Signature: ___________________________ Date: ____________`

