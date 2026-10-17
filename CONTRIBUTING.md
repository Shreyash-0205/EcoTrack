# Contributing to EcoTrack

Thank you for your interest in contributing to **EcoTrack — Smart Waste Management and Segregation System**! EcoTrack is an open-source civic engineering project built to foster collaborative, transparent waste management and responsible segregation.

---

## Code of Conduct

All contributors and maintainers are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md). Please ensure respectful and inclusive communication at all times.

---

## How to Contribute to EcoTrack

### 1. Development Setup
1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/ecotrack.git
   cd ecotrack
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # Linux / macOS:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Seed demo data:
   ```bash
   python seed_data.py
   ```
5. Run the development server:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

### 2. Running Automated Tests
Run the pytest test suite before committing changes:
```bash
pytest
```
Ensure all 34+ automated tests pass with 0 failures.

### 3. Submitting Pull Requests
1. Branch from `main` using descriptive branch naming (`fix/image-upload-bounds`, `feat/export-csv-reports`, `docs/gantt-chart-update`).
2. Adhere to **PEP 8** conventions for Python backend code.
3. Keep frontend templates accessible: use semantic HTML, accessible color contrast ratios (WCAG 2.1 AA), and descriptive `aria-` labels.
4. Ensure no hardcoded credentials or debug secrets are committed.
5. Submit your PR using the repository's [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md).

---

## Contributing to Upstream & Peer Open-Source Projects

As part of the University of Mumbai open-source engineering curriculum, student teams are encouraged to explore and contribute to established open-source civic and environmental projects. Below are verified open-source initiatives:

### 1. OpenStreetMap (OSM)
- **Repository:** [https://github.com/openstreetmap/openstreetmap-website](https://github.com/openstreetmap/openstreetmap-website)
- **Domain:** Global crowd-sourced geospatial mapping data.
- **Genuine Contribution Opportunities:**
  - Tagging and verifying municipal dry waste collection kiosks and recycling centers in regional Indian wards (e.g., using `amenity=recycling`, `recycling:plastic=yes`).
  - Fixing frontend accessibility issues in the web interface.
  - Adding automated tests for geospatial boundary lookups.

### 2. OpenAQ
- **Repository:** [https://github.com/openaq/openaq-backend](https://github.com/openaq/openaq-backend)
- **Domain:** Community-driven global air quality and environmental data.
- **Genuine Contribution Opportunities:**
  - Submitting data parsers for localized Indian municipal sensor feeds.
  - Expanding automated integration tests and API documentation.
  - Resolving open good-first-issues on GitHub.

### 3. Public Lab (plots2)
- **Repository:** [https://github.com/publiclab/plots2](https://github.com/publiclab/plots2)
- **Domain:** Community science and civic environmental investigation platform.
- **Genuine Contribution Opportunities:**
  - Contributing to introductory "first-timers-only" labeled issues.
  - Writing unit tests for image preview modules and form input validation.
  - Translating educational environmental guides into regional Indian languages (Hindi, Marathi).

> **Academic Ethics Notice:** Students must never claim that a pull request, issue, or contribution has been submitted unless genuine pull request links and commits exist on GitHub. Authentic contributions should be verified by project mentors before inclusion in final examination portfolios.

