# EcoTrack Project Roadmap

This roadmap outlines current accomplishments and future milestones for the **EcoTrack** smart waste management platform.

---

## Phase 1: Core Civic Foundation (Completed — v1.0.0)

- [x] Full-stack architecture using Python 3.13, Flask 3.1, SQLite, and Bootstrap 5.3.
- [x] Secure user authentication (Citizen and Administrator roles) with password hashing.
- [x] Waste hotspot reporting with category tagging (Wet, Dry, Plastic, E-waste, Mixed, Other).
- [x] Interactive Leaflet.js map with OpenStreetMap tiles and status-colored pins.
- [x] Coordinate picker and HTML5 geolocation support for mobile devices.
- [x] Safe photograph uploads with extension whitelisting, 5MB limit, and Pillow binary verification.
- [x] Comprehensive Educational Waste Segregation Guide with municipal disclaimer.
- [x] Administrative Console for status triage, field notes, and duplicate deletion.
- [x] Immutable activity logs tracking administrative interventions.
- [x] Automated test suite (34 passing pytest tests) covering auth, reports, security, and DB.

---

## Phase 2: Enhanced Civic Governance (Target: Q3 2026)

- [ ] **Municipal Ward Boundaries:** Overlay GeoJSON polygons for Greater Mumbai administrative wards (e.g., Ward A, G/North, K/West) on the Leaflet map.
- [ ] **Multi-Lingual Localization:** Implement internationalization (i18n) for Hindi and Marathi language support to enhance accessibility across diverse demographic groups.
- [ ] **Citizen Feedback Loop:** Enable citizens to mark whether they are satisfied with resolved cleanup operations.
- [ ] **CSV / PDF Export:** Allow administrative officers to export monthly ward compliance summaries in tabular CSV and printable PDF formats.

---

## Phase 3: AI & Edge Intelligence (Target: Q4 2026)

- [ ] **On-Device Waste Classification:** Integrate a client-side lightweight machine learning model (TensorFlow.js or ONNX) to suggest categories (Wet/Plastic/E-waste) when a citizen captures a waste photo.
- [ ] **Duplicate Detection:** Use perceptual image hashing (`imagehash`) and geographic clustering (DBSCAN) to detect duplicate reports within 50 meters of an existing active hotspot.
- [ ] **Notification Webhooks:** Provide optional webhooks for integration with municipal Telegram or WhatsApp civic bots (configured via local API tokens).

---

## Phase 4: Offline Field Capabilities (Target: 2027)

- [ ] **Progressive Web App (PWA):** Service worker caching and offline report storage using browser `IndexedDB`.
- [ ] **Automatic Background Sync:** Queue reports captured in low-reception basement or alleyway areas and upload when network connectivity restores.
- [ ] **Route Optimization for Collection Trucks:** Graph-based traveling salesperson route calculation between confirmed hotspots using open-source OpenRouteService / OSRM.

