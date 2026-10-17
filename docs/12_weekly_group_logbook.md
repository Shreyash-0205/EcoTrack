# 12. Weekly Group Logbook (8-Week Academic Project Record)

**Project Title:** EcoTrack — Smart Waste Management and Segregation System  
**Academic Year:** 2026 | **Semester:** VII  
**Course:** B.E. Computer Engineering / Information Technology  
**University:** University of Mumbai  

---

### Week 1: Project Initiation & Problem Definition
- **Date Range:** Week 1 (Days 1–7)
- **Weekly Objective:** Finalize civic domain problem statement, review Mumbai solid waste challenges, and establish open-source repository foundation.
- **Individual Contributions:**
  - *Student 1 (Backend/DB):* Setup Git repository, configured `.gitignore`, and authored initial `config.py` skeleton.
  - *Student 2 (Frontend/UI):* Researched WCAG 2.1 accessibility guidelines and formulated eco-friendly color palette (forest green, emerald, white).
  - *Student 3 (Testing/Docs):* Drafted initial project charter and compiled survey of CPHEEO and SWM 2016 rules.
  - *Student 4 (Maps/Analytics):* Investigated free mapping engines (Leaflet.js + OSM) to eliminate paid API requirements.
- **Faculty Guide Guidance:** Advised ensuring all report data distinctions between demo data and real submissions are clearly maintained.
- **Guide Signature Placeholder:** `[  Prof. Guide Signature: __________________  Date: ________  ]`

---

### Week 2: Requirements Analysis & System Modeling
- **Date Range:** Week 2 (Days 8–14)
- **Weekly Objective:** Establish formal Functional & Non-Functional requirements and construct UML/DFD models.
- **Individual Contributions:**
  - *Student 1:* Formulated relational database schema for `users`, `reports`, and `activity_logs`.
  - *Student 2:* Created HTML/CSS mockups and wireframes for mobile and desktop screens.
  - *Student 3:* Developed Use-Case and DFD Level 0 and Level 1 diagrams using Mermaid.
  - *Student 4:* Evaluated OpenStreetMap raster tile server limits and GeoJSON payload structures.
- **Faculty Guide Guidance:** Recommended incorporating an educational waste segregation guide directly within the web app.
- **Guide Signature Placeholder:** `[  Prof. Guide Signature: __________________  Date: ________  ]`

---

### Week 3: Database Implementation & Authentication Engine
- **Date Range:** Week 3 (Days 15–21)
- **Weekly Objective:** Implement SQLAlchemy ORM models, password hashing, and user authentication sessions.
- **Individual Contributions:**
  - *Student 1:* Coded `models/user.py`, `models/report.py`, and `models/activity_log.py` with foreign key cascades.
  - *Student 2:* Built responsive registration and login templates (`login.html`, `register.html`).
  - *Student 3:* Created session validation helpers and automated tests for password hashing (`test_auth.py`).
  - *Student 4:* Implemented role-based routing middleware (`@login_required` and `@admin_required`).
- **Guide Signature Placeholder:** `[  Prof. Guide Signature: __________________  Date: ________  ]`

---

### Week 4: Waste Reporting Form & Safe File Upload Pipeline
- **Date Range:** Week 4 (Days 22–28)
- **Weekly Objective:** Implement the citizen hotspot submission form with photo verification and coordinates.
- **Individual Contributions:**
  - *Student 1:* Created `routes/citizen.py` for `/report` and `/my-reports`.
  - *Student 2:* Implemented client-side image preview and 5MB validation in `main.js`.
  - *Student 3:* Developed Pillow-based binary image verification (`save_uploaded_image`) in `utils/security.py`.
  - *Student 4:* Integrated HTML5 Geolocation API with latitude/longitude inputs.
- **Guide Signature Placeholder:** `[  Prof. Guide Signature: __________________  Date: ________  ]`

---

### Week 5: Geospatial Leaflet Mapping & Hotspot Filtering
- **Date Range:** Week 5 (Days 29–35)
- **Weekly Objective:** Build interactive Leaflet.js map with custom status markers and coordinate picker.
- **Individual Contributions:**
  - *Student 1:* Built `/api/reports` JSON endpoint supporting category and status query parameters.
  - *Student 2:* Designed custom CSS pin markers (`map-marker-reported`, `map-marker-resolved`, etc.).
  - *Student 3:* Developed automated tests verifying coordinates boundary validation (-90 to 90, -180 to 180).
  - *Student 4:* Implemented `initMainMap` and `initPickerMap` in `static/js/map.js`.
- **Guide Signature Placeholder:** `[  Prof. Guide Signature: __________________  Date: ________  ]`

---

### Week 6: Administrator Triage & Immutable Audit Logs
- **Date Range:** Week 6 (Days 36–42)
- **Weekly Objective:** Implement administrative status lifecycle controls, field notes, and audit logging.
- **Individual Contributions:**
  - *Student 1:* Developed `/admin/reports/<id>/status` and `/admin/reports/<id>/delete` routes with activity triggers.
  - *Student 2:* Designed `manage_reports.html` table with inline modal dialogs for status updates.
  - *Student 3:* Created `ActivityLog` model and audit view template (`logs.html`).
  - *Student 4:* Built multi-criteria search (title, landmark, reporter) with pagination.
- **Guide Signature Placeholder:** `[  Prof. Guide Signature: __________________  Date: ________  ]`

---

### Week 7: Chart.js Analytics & Comprehensive Test Suite
- **Date Range:** Week 7 (Days 43–49)
- **Weekly Objective:** Integrate Chart.js visualizations and achieve 100% test pass rate with pytest.
- **Individual Contributions:**
  - *Student 1:* Optimized SQL queries to modernize `db.session.get()` and reduce database round-trips.
  - *Student 2:* Built responsive doughnut and bar charts for waste categories and status funnels.
  - *Student 3:* Authored full 34-test suite covering auth, reports, admin, security, and DB constraints.
  - *Student 4:* Added realistic Mumbai metropolitan seed dataset in `seed_data.py`.
- **Guide Signature Placeholder:** `[  Prof. Guide Signature: __________________  Date: ________  ]`

---

### Week 8: Documentation, Verification & Final Presentation
- **Date Range:** Week 8 (Days 50–56)
- **Weekly Objective:** Finalize academic documentation, verify zero-warning test execution, and prepare demo.
- **Individual Contributions:**
  - *All Team Members:* Conducted end-to-end integration testing, verified live Leaflet map rendering, compiled university mini-project report, and prepared project defense presentation.
- **Guide Signature Placeholder:** `[  Prof. Guide Signature: __________________  Date: ________  ]`

