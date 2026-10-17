# 5. Literature and Repository Survey

## 5.1 Academic Literature Survey

1. **CPHEEO (Central Public Health and Environmental Engineering Organisation), 2016:**
   *Manual on Municipal Solid Waste Management*, Ministry of Housing and Urban Affairs, Government of India.
   - *Key Insight:* Outlines the critical necessity of three-way and multi-stream source segregation. Unsegregated garbage dumped in open landfills generates methane gas and leachate that contaminates urban aquifers.
   - *System Alignment:* EcoTrack enforces categorical classification at the point of citizen reporting.

2. **Joshi, R. and Ahmed, S. (2016):**
   "Status and Challenges of Municipal Solid Waste Management in India: A Review", *Cogent Environmental Science*, Vol. 2, No. 1.
   - *Key Insight:* Highlights the acute shortage of real-time geospatial monitoring in urban local bodies. The paper advocates for digital crowd-sourced reporting systems to optimize municipal collection routing.
   - *System Alignment:* EcoTrack incorporates OpenStreetMap and Leaflet.js to pinpoint hotspots on interactive maps without commercial API costs.

3. **Open Geospatial Consortium (OGC) Standards:**
   - *Key Insight:* Open spatial data standards (WGS84 coordinate systems and GeoJSON specifications) provide robust interoperability across diverse web frameworks.
   - *System Alignment:* EcoTrack's `/api/reports` serves standardized JSON payloads compatible with open GIS clients.

---

## 5.2 Open-Source Repository Survey

| Repository Name | Primary Domain | Core Tech Stack | Verified Repository URL | Key Takeaways for EcoTrack |
| :--- | :--- | :--- | :--- | :--- |
| **OpenStreetMap Website** | Open-source geographic mapping & cartography | Ruby on Rails, Leaflet.js, PostgreSQL/PostGIS | `https://github.com/openstreetmap/openstreetmap-website` | Utilized Leaflet.js rendering patterns and OSM tile server configuration; zero commercial API keys required. |
| **OpenAQ Backend** | Open environmental & air quality monitoring | Python, FastAPI, PostgreSQL, AWS | `https://github.com/openaq/openaq-backend` | Demonstrated best practices for structured REST API endpoints and data filtering by category and date. |
| **Public Lab (plots2)** | Community science and civic environmental reporting | Ruby, JavaScript, Leaflet | `https://github.com/publiclab/plots2` | Informed our approach to community-driven environmental investigation, image verification, and accessible UI. |
| **FixMyStreet (mySociety)** | Civic street and infrastructure reporting | Perl, PostgreSQL, Leaflet | `https://github.com/mysociety/fixmystreet` | Validated the utility of public status transitions (Reported &rarr; In Progress &rarr; Fixed) for citizen trust. |

> **Academic Ethics Note:** The repositories surveyed above are real, established open-source projects. URLs and technical stacks have been verified. Students referencing these repositories for semester lab submissions should inspect open issues and contribute documentation or test improvements following upstream guidelines.

