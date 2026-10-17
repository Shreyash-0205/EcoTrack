/**
 * EcoTrack — Main JavaScript Application
 * Handles UI interactions, client-side validation, and flash messages.
 */

document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 6000);
    });

    // Image upload preview and client-side size check
    const photoInput = document.getElementById('photo-input');
    const photoPreviewContainer = document.getElementById('photo-preview-container');
    const photoPreview = document.getElementById('photo-preview');

    if (photoInput && photoPreviewContainer && photoPreview) {
        photoInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                // Client-side 5MB limit check
                if (file.size > 5 * 1024 * 1024) {
                    alert('Selected image exceeds the 5MB file size limit. Please choose a smaller photo.');
                    this.value = '';
                    photoPreviewContainer.style.display = 'none';
                    return;
                }

                // Check allowed extensions
                const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
                if (!validTypes.includes(file.type)) {
                    alert('Invalid file format. Please select a JPG, PNG, or WEBP image.');
                    this.value = '';
                    photoPreviewContainer.style.display = 'none';
                    return;
                }

                const reader = new FileReader();
                reader.onload = function (e) {
                    photoPreview.src = e.target.result;
                    photoPreviewContainer.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                photoPreviewContainer.style.display = 'none';
            }
        });
    }

    // Geolocation trigger button on reporting form
    const btnGetLocation = document.getElementById('btn-get-location');
    const latInput = document.getElementById('latitude-input');
    const lngInput = document.getElementById('longitude-input');
    const locationStatus = document.getElementById('geo-status');

    if (btnGetLocation && latInput && lngInput) {
        btnGetLocation.addEventListener('click', function () {
            if (!navigator.geolocation) {
                if (locationStatus) locationStatus.innerText = 'Geolocation is not supported by your browser.';
                return;
            }

            btnGetLocation.disabled = true;
            btnGetLocation.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Locating...';
            if (locationStatus) locationStatus.innerText = 'Acquiring GPS coordinates...';

            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const lat = position.coords.latitude.toFixed(6);
                    const lng = position.coords.longitude.toFixed(6);
                    latInput.value = lat;
                    lngInput.value = lng;
                    if (locationStatus) {
                        locationStatus.className = 'text-success small mt-1';
                        locationStatus.innerText = `Coordinates locked: ${lat}, ${lng}`;
                    }
                    btnGetLocation.disabled = false;
                    btnGetLocation.innerHTML = '<i class="bi bi-geo-alt-fill"></i> Location Acquired';

                    // If picker map is present, update pin
                    if (window.updatePickerMarker) {
                        window.updatePickerMarker(parseFloat(lat), parseFloat(lng));
                    }
                },
                function (error) {
                    btnGetLocation.disabled = false;
                    btnGetLocation.innerHTML = '<i class="bi bi-geo-alt"></i> Use My Location';
                    let errorMsg = 'Unable to retrieve location.';
                    if (error.code === error.PERMISSION_DENIED) {
                        errorMsg = 'Location permission denied by user.';
                    } else if (error.code === error.POSITION_UNAVAILABLE) {
                        errorMsg = 'Location information is currently unavailable.';
                    } else if (error.code === error.TIMEOUT) {
                        errorMsg = 'Location request timed out.';
                    }
                    if (locationStatus) {
                        locationStatus.className = 'text-warning small mt-1';
                        locationStatus.innerText = errorMsg;
                    }
                },
                { timeout: 10000, enableHighAccuracy: true }
            );
        });
    }
});

