# 3. Objectives and Scope

## 3.1 Project Objectives
1. **Centralized Hotspot Reporting:**
   Develop an intuitive, mobile-responsive web portal where citizens can submit complaints regarding unattended waste within seconds.
2. **Standardized Waste Stream Categorization:**
   Implement source categorization into Wet, Dry, Plastic, E-waste, and Mixed waste streams aligned with India's Solid Waste Management Rules (2016).
3. **Geospatial Tracking without Commercial APIs:**
   Integrate Leaflet.js and OpenStreetMap (OSM) tile layers to map reported garbage spots without reliance on paid services such as Google Maps Platform.
4. **Transparent Status Lifecycle & Audit Trail:**
   Provide a closed-loop resolution workflow (Reported &rarr; In Progress &rarr; Resolved / Rejected) with administrator field notes and automated audit logs.
5. **Educational Civic Awareness:**
   Deliver a comprehensive, responsive waste segregation guide highlighting what belongs in each waste stream and addressing local municipal variations.
6. **Open-Source Engineering Best Practices:**
   Enforce clean modular architecture, PEP 8 styling, automated test coverage using `pytest`, security hardening (CSRF, password hashing, safe file uploads), and open-source licensing (MIT).

## 3.2 Scope of the System
### In Scope:
- User registration, session authentication, and role-based access control (Citizen vs. Administrator).
- Hotspot submission with mandatory landmark, description, category, and optional GPS coordinates and photograph.
- Interactive Leaflet coordinate picker with HTML5 device geolocation.
- Dynamic filtering of map pins and report tables by category and status.
- Administrative triage console with audit logging of all modifications and deletions.
- Automated testing suite and Mumbai University documentation templates.

### Out of Scope (Future Milestones):
- Hardware-based IoT fill-level sensors in municipal smart bins (simulated via citizen reports).
- Payment gateways for municipal sanitation fines or commercial recycling transactions.
- Automated satellite image classification (relies on crowd-sourced photographs).

