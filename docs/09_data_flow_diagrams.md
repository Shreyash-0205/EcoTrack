# 9. Data-Flow Diagrams (DFD)

## 9.1 DFD Level 0 — Context Diagram
The Level 0 context diagram demonstrates the boundary of the EcoTrack application with respect to external entities: Citizens, Civic Administrators, and OpenStreetMap.

```mermaid
flowchart LR
    Citizen["Citizen"]
    System(("0.0<br>EcoTrack System"))
    Admin["Civic Administrator"]
    OSM["OpenStreetMap Server"]

    Citizen -->|"Registration & Login Credentials"| System
    Citizen -->|"Hotspot Reports, Coordinates, Photos"| System
    System -->|"Status Updates & Notification Alerts"| Citizen

    Admin -->|"Admin Login Credentials"| System
    Admin -->|"Status Updates, Field Notes, Deletions"| System
    System -->|"Aggregate Stats & Audit Trail Logs"| Admin

    OSM -->|"OpenStreetMap Map Tile PNGs"| System
    System -->|"Rendered Map View to Browser"| Citizen
```

---

## 9.2 DFD Level 1 — Detailed Process Decomposition

```mermaid
flowchart TD
    Citizen["Citizen"]
    Admin["Civic Administrator"]

    subgraph Processes["EcoTrack Processes"]
        P1(("1.0<br>User Auth & Session Management"))
        P2(("2.0<br>Report Ingestion & Image Processing"))
        P3(("3.0<br>Geospatial Querying & Map Filtering"))
        P4(("4.0<br>Admin Triage & Status Control"))
        P5(("5.0<br>Audit Trail Recording"))
    end

    subgraph DataStores["Data Stores"]
        D1[("D1: Users Store")]
        D2[("D2: Reports Store")]
        D3[("D3: Activity Logs Store")]
        D4[("D4: Physical Uploads")]
    end

    Citizen -->|"Credentials"| P1
    P1 <-->|"Verify & Hash Password"| D1
    P1 -->|"Session Established"| Citizen

    Citizen -->|"Report Data & Photo"| P2
    P2 -->|"Validated Report Record"| D2
    P2 -->|"Secure UUID Image"| D4
    P2 -->|"Complaint Confirmation"| Citizen

    D2 -->|"Geo Reports Query"| P3
    P3 -->|"Filtered GeoJSON"| Citizen

    Admin -->|"Credentials"| P1
    Admin -->|"Status & Notes"| P4
    P4 <-->|"Read / Update Reports"| D2
    P4 -->|"Trigger Audit Event"| P5
    P5 -->|"Append Immutable Log"| D3
    D3 -->|"Audit History Feed"| Admin
```

---

## 9.3 Data Dictionary Summary
- **User Record:** `{id, name, email, password_hash, role, created_at}`
- **Report Record:** `{id, user_id, title, description, category, location, latitude, longitude, image_filename, status, admin_notes, is_demo, created_at, updated_at}`
- **Activity Log Record:** `{id, admin_user_id, report_id, action, details, created_at}`
- **Uploaded Image Payload:** `{uuid_filename, raw_bytes, mime_type, file_size}`

