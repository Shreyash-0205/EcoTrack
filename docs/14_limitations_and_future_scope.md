# 14. Limitations and Future Scope

## 14.1 Limitations of the Current Implementation
While EcoTrack delivers a fully functional, tested, and secure prototype, several technical and operational boundaries exist:

1. **Local SQLite Persistence:**
   SQLite is well-suited for single-process, local demonstration, and undergraduate academic evaluation. However, concurrent write contention under tens of thousands of simultaneous municipal requests would necessitate migration to a client-server RDBMS (e.g., PostgreSQL with PostGIS).

2. **Network Dependency for Map Tiles:**
   While the application core and cached assets operate locally, rendering detailed OpenStreetMap cartography requires active internet connectivity to fetch OSM raster tiles.

3. **Manual Category Assignment:**
   Citizens must choose the waste category manually. Although an educational guide is provided, misclassification may occasionally occur due to user error.

4. **Manual Duplicate Triage:**
   Duplicate reports submitted by multiple neighbors regarding the same hotspot must currently be reviewed and deleted manually by the administrator.

5. **Single-Node File Storage:**
   Uploaded photographs are stored directly in the local file system (`uploads/reports/`). A high-availability production deployment would require an S3-compatible open-source object storage solution (such as MinIO).

---

## 14.2 Future Scope & Research Directions

1. **On-Device Computer Vision (Edge AI):**
   Integrate a lightweight TensorFlow.js or ONNX model directly inside the browser to analyze photos in real-time and automatically recommend waste streams (e.g., detecting PET bottles or cardboard).

2. **Spatial Clustering & Duplicate Detection:**
   Implement geospatial clustering algorithms (such as DBSCAN or PostGIS `ST_DWithin`) to automatically group reports originating within 25–50 meters of one another into a single aggregated incident.

3. **Offline Progressive Web App (PWA):**
   Utilize Service Workers, the Cache API, and IndexedDB to allow field sanitation workers to record inspections in offline basements and automatically sync once network reception is regained.

4. **Automated Vehicle Routing (Green Logistics):**
   Integrate open-source routing engines (such as Open Source Routing Machine / OSRM or OpenRouteService) to compute shortest-path cleanup routes for municipal compactor trucks based on active hotspot coordinates.

5. **Multi-Lingual Localization (i18n):**
   Introduce localized user interfaces in Marathi and Hindi using Flask-Babel to maximize adoption across regional ward populations.

