# 4. Existing System vs. Proposed System

## 4.1 Analysis of the Existing System
In many Indian urban local bodies, civic complaint handling relies either on traditional offline channels or fragmented municipal apps:

| Parameter | Existing System | Limitations |
| :--- | :--- | :--- |
| **Submission Medium** | Physical complaints register, toll-free hotlines, or generic municipal grievance portals. | High friction; requires manual telephone queuing or travel to ward offices during work hours. |
| **Categorization** | Generic complaint categories (e.g., "Debris" or "Garbage"). | Fails to distinguish between organic wet waste, plastics, or toxic electronic items. |
| **Location Precision** | Approximate text descriptions ("Near main junction"). | Ambiguity results in sanitation trucks searching wide areas; no GPS pin drops. |
| **Visual Evidence** | Generally not supported or poorly handled without size validation. | Municipal supervisors cannot assess dump scale prior to dispatching crews. |
| **Transparency** | One-way status ("Received" or "Closed") with no detailed field notes. | Citizens have no insight into when or how their complaint was addressed. |
| **Technology Dependency** | Proprietary corporate systems or expensive commercial map licensing. | Cost-prohibitive for smaller municipalities and non-extensible for student researchers. |

---

## 4.2 Proposed System (EcoTrack)
EcoTrack establishes a modern, transparent, community-driven civic platform:

| Parameter | Proposed System (EcoTrack) | Advantages |
| :--- | :--- | :--- |
| **Accessibility** | Responsive web application accessible across mobile phones, tablets, and desktops. | Instant access without needing heavy app store downloads. |
| **Waste Stream Segregation** | 5 discrete waste streams (Wet, Dry, Plastic, E-waste, Mixed/Other). | Ensures appropriate crew assignment (e.g., composters vs. e-waste dismantlers). |
| **Mapping Engine** | Leaflet.js with OpenStreetMap (OSM) tile rendering. | 100% free and open-source; zero paid API limits or licensing charges. |
| **Coordinate Capture** | Interactive map pin-drop picker + HTML5 browser GPS button. | Precise coordinates down to meter-level accuracy. |
| **Visual Verification** | Secure photo upload pipeline with Pillow binary validation. | Prevents malware execution while providing visual verification to authorities. |
| **Operational Audit** | Immutable administrative activity log with timestamps. | Enforces civic accountability for every status transition and note. |
| **Education Module** | Integrated Waste Segregation Guide. | Promotes scientific segregation at source with local municipal adaptability notes. |

