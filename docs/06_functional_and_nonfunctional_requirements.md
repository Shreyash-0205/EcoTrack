# 6. Functional and Non-Functional Requirements

## 6.1 Functional Requirements (FR)

- **FR-01: User Authentication & Role Management:**
  The system must provide registration and login mechanisms for citizens and administrators, generating secure password hashes via Werkzeug (`scrypt`).
- **FR-02: Waste Hotspot Reporting:**
  Citizens must be able to submit reports specifying a title (5–150 chars), detailed description (10+ chars), category, physical landmark, optional coordinates, and optional photo.
- **FR-03: Waste Stream Categorization:**
  The application must enforce categorization into one of six valid streams: Wet, Dry, Plastic, E-waste, Mixed, or Other.
- **FR-04: Interactive Map Pin Drop & Geolocation:**
  The reporting interface must allow users to drop a pin on a Leaflet map or click "Use My Current Location" via the HTML5 Geolocation API to auto-fill decimal coordinates.
- **FR-05: Safe Image Uploads:**
  The backend must validate file extensions against `{.jpg, .jpeg, .png, .webp}`, enforce a 5 MB file size limit, verify image binary headers using Pillow, and rename files with unique UUIDs.
- **FR-06: Interactive Hotspot Map View:**
  The system must display reports with valid coordinates on OpenStreetMap using Leaflet.js, color-coded by status with clickable popups containing photos, details, and links.
- **FR-07: Report Search and Multi-Criteria Filtering:**
  Citizens and administrators must be able to filter reports by category, status, search keyword, and creation date.
- **FR-08: Administrative Status Triage:**
  Authorized administrators must be able to update report status (Reported &rarr; In Progress &rarr; Resolved / Rejected) and append administrative field notes.
- **FR-09: Immutable Audit Logging:**
  Every administrative intervention (status change, notes update, or report deletion) must generate an automated audit log entry with timestamp and admin ID.
- **FR-10: Waste Segregation Educational Guide:**
  The system must deliver an accessible guide covering organic compostables, recyclables, plastics, e-waste, and hazardous waste with municipal compliance notices.

---

## 6.2 Non-Functional Requirements (NFR)

- **NFR-01: Security & Confidentiality:**
  All POST endpoints must validate session-bound CSRF tokens. Plaintext passwords must never be stored. Administrative routes must strictly enforce server-side RBAC decorators.
- **NFR-02: Usability and Responsiveness:**
  The interface must be fully responsive across desktop, tablet, and mobile screens (viewport widths from 360px to 1920px) using Bootstrap 5 grid systems and accessible WCAG 2.1 AA color contrast ratios.
- **NFR-03: Performance:**
  Page loads and API JSON responses (`/api/reports`) must execute within sub-second thresholds (< 500 ms) under local server operation.
- **NFR-04: Reliability and Data Integrity:**
  Foreign keys with `ON DELETE CASCADE` or `SET NULL` must maintain referential integrity in SQLite. Application errors must display user-friendly error templates without leaking stack traces.
- **NFR-05: Zero Commercial Dependency:**
  The entire architecture must function without proprietary paid APIs (using OpenStreetMap instead of Google Maps, SQLite instead of commercial cloud DBs).
- **NFR-06: Testability:**
  Core workflows must be covered by automated test scripts executable via `pytest` with reproducible test assertions.

