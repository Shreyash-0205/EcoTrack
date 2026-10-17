/**
 * EcoTrack — Leaflet Map Integration
 * Manages OpenStreetMap layers, dynamic status-colored markers, popups, and coordinate pickers.
 */

// Helper to construct custom HTML markers based on report status
function createStatusIcon(status) {
    let pinClass = 'map-marker-reported';
    if (status === 'In Progress') pinClass = 'map-marker-inprogress';
    else if (status === 'Resolved') pinClass = 'map-marker-resolved';
    else if (status === 'Rejected') pinClass = 'map-marker-rejected';

    return L.divIcon({
        className: 'custom-div-icon',
        html: `<div class="map-marker-pin ${pinClass}"></div>`,
        iconSize: [30, 42],
        iconAnchor: [15, 42],
        popupAnchor: [0, -38]
    });
}

// 1. Main Interactive Map for /map page
function initMainMap() {
    const mapElement = document.getElementById('main-map');
    if (!mapElement) return;

    // Default center Mumbai region
    const defaultCoords = [19.0760, 72.8777];
    const map = L.map('main-map').setView(defaultCoords, 11);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    let markersLayer = L.layerGroup().addTo(map);

    function fetchAndRenderReports() {
        const categorySelect = document.getElementById('filter-category');
        const statusSelect = document.getElementById('filter-status');
        const searchInput = document.getElementById('filter-search');

        const category = categorySelect ? categorySelect.value : '';
        const status = statusSelect ? statusSelect.value : '';
        const search = searchInput ? searchInput.value.trim() : '';

        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (status) params.append('status', status);
        if (search) params.append('q', search);

        const url = `/api/reports?${params.toString()}`;

        // Visual loading indicator on map counter
        const counterBadge = document.getElementById('map-reports-count');
        if (counterBadge) counterBadge.innerText = 'Loading...';

        fetch(url)
            .then(res => res.json())
            .then(data => {
                markersLayer.clearLayers();
                const reports = data.reports || [];

                if (counterBadge) {
                    counterBadge.innerText = `${reports.length} Hotspots on Map`;
                }

                const markerCoords = [];

                reports.forEach(report => {
                    if (report.has_coordinates && report.latitude !== null && report.longitude !== null) {
                        const icon = createStatusIcon(report.status);
                        const marker = L.marker([report.latitude, report.longitude], { icon: icon });

                        const imgUrl = report.image_url || report.fallback_image_url || '/static/images/fallbacks/other.svg';
                        const fallbackUrl = report.fallback_image_url || '/static/images/fallbacks/other.svg';
                        const categorySlug = report.category_slug || 'other';

                        const imageHtml = `
                            <div class="mt-2 text-center rounded overflow-hidden fallback-bg-${categorySlug}" style="height: 105px; border: 1px solid rgba(0,0,0,0.06);">
                                <img src="${imgUrl}" 
                                     alt="${report.category || 'Waste'} Photo" 
                                     style="width: 100%; height: 100%; object-fit: cover; display: block;"
                                     onerror="this.onerror=null; this.src='${fallbackUrl}';">
                            </div>
                        `;

                        const popupHtml = `
                            <div class="map-popup-card" style="min-width: 210px; max-width: 260px;">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <span class="badge ${report.status_badge_class || 'bg-secondary text-white'}" style="font-size: 0.75rem;">${report.status}</span>
                                    <span class="badge ${report.category_badge_class || 'badge-category-other'}" style="font-size: 0.75rem;">${report.category}</span>
                                </div>
                                <h6 class="fw-bold mb-1 mt-2 text-dark" style="font-size: 0.95rem;">${report.title}</h6>
                                <p class="text-muted small mb-1" style="font-size: 0.8rem;">
                                    <i class="bi bi-geo-alt"></i> ${report.location}
                                </p>
                                ${imageHtml}
                                <div class="d-flex justify-content-between align-items-center mt-2 pt-2 border-top">
                                    <small class="text-muted" style="font-size: 0.75rem;">${report.created_at}</small>
                                    <a href="/reports/${report.id}" class="btn btn-sm btn-outline-success py-0 px-2" style="font-size: 0.75rem;">
                                        View Details
                                    </a>
                                </div>
                            </div>
                        `;

                        marker.bindPopup(popupHtml);
                        markersLayer.addLayer(marker);
                        markerCoords.push([report.latitude, report.longitude]);
                    }
                });

                // Auto-fit bounds if markers exist
                if (markerCoords.length > 0) {
                    map.fitBounds(markerCoords, { padding: [40, 40], maxZoom: 14 });
                }
            })
            .catch(err => {
                console.error("Failed to load map reports:", err);
                if (counterBadge) counterBadge.innerText = 'Error loading markers';
            });
    }

    // Event listeners for filters
    const filterBtn = document.getElementById('btn-apply-filters');
    const resetBtn = document.getElementById('btn-reset-filters');
    const categorySelect = document.getElementById('filter-category');
    const statusSelect = document.getElementById('filter-status');

    if (filterBtn) filterBtn.addEventListener('click', fetchAndRenderReports);
    if (categorySelect) categorySelect.addEventListener('change', fetchAndRenderReports);
    if (statusSelect) statusSelect.addEventListener('change', fetchAndRenderReports);

    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            if (categorySelect) categorySelect.value = '';
            if (statusSelect) statusSelect.value = '';
            const searchInput = document.getElementById('filter-search');
            if (searchInput) searchInput.value = '';
            fetchAndRenderReports();
        });
    }

    // Initial load
    fetchAndRenderReports();
}

// 2. Interactive Coordinate Picker Map on Report Submission Form
function initPickerMap() {
    const mapElement = document.getElementById('picker-map');
    if (!mapElement) return;

    const latInput = document.getElementById('latitude-input');
    const lngInput = document.getElementById('longitude-input');
    const locationStatus = document.getElementById('geo-status');

    let initialLat = 19.0760;
    let initialLng = 72.8777;

    if (latInput && latInput.value && lngInput && lngInput.value) {
        const parsedLat = parseFloat(latInput.value);
        const parsedLng = parseFloat(lngInput.value);
        if (!isNaN(parsedLat) && !isNaN(parsedLng)) {
            initialLat = parsedLat;
            initialLng = parsedLng;
        }
    }

    const pickerMap = L.map('picker-map').setView([initialLat, initialLng], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(pickerMap);

    let pickerMarker = null;

    function placePin(lat, lng) {
        if (pickerMarker) {
            pickerMarker.setLatLng([lat, lng]);
        } else {
            pickerMarker = L.marker([lat, lng], { draggable: true }).addTo(pickerMap);
            pickerMarker.on('dragend', function (e) {
                const pos = e.target.getLatLng();
                updateInputs(pos.lat, pos.lng);
            });
        }
    }

    function updateInputs(lat, lng) {
        const fixedLat = lat.toFixed(6);
        const fixedLng = lng.toFixed(6);
        if (latInput) latInput.value = fixedLat;
        if (lngInput) lngInput.value = fixedLng;
        if (locationStatus) {
            locationStatus.className = 'text-success small mt-1';
            locationStatus.innerText = `Pin dropped: ${fixedLat}, ${fixedLng}`;
        }
    }

    // If initial values already existed, place marker
    if (latInput && latInput.value && lngInput && lngInput.value) {
        placePin(initialLat, initialLng);
    }

    // Click on map to drop or move pin
    pickerMap.on('click', function (e) {
        placePin(e.latlng.lat, e.latlng.lng);
        updateInputs(e.latlng.lat, e.latlng.lng);
    });

    // Expose global updater for geolocation button in main.js
    window.updatePickerMarker = function (lat, lng) {
        placePin(lat, lng);
        pickerMap.setView([lat, lng], 15);
    };
}

// 3. Detail Map for Single Report View
function initDetailMap(lat, lng, title) {
    const mapElement = document.getElementById('detail-map');
    if (!mapElement || isNaN(lat) || isNaN(lng)) return;

    const detailMap = L.map('detail-map').setView([lat, lng], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(detailMap);

    const marker = L.marker([lat, lng]).addTo(detailMap);
    marker.bindPopup(`<strong>${title}</strong><br>Coordinates: ${lat}, ${lng}`).openPopup();
}

// DOM ready initialization
document.addEventListener('DOMContentLoaded', function () {
    initMainMap();
    initPickerMap();
});

