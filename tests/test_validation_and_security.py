"""
Automated tests for input validation, safe file uploads, and web security.
"""
import io
from models import db, Report


def test_invalid_category_rejected(auth_citizen_client):
    """Submitting an invalid waste category is rejected by backend validation."""
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Test Invalid Category',
        'category': 'RadioactiveFuel',
        'location': 'Industrial Ward',
        'description': 'Valid long description of waste hotspot.'
    }, follow_redirects=True)

    assert b"Please select a valid waste category" in response.data


def test_short_title_rejected(auth_citizen_client):
    """Title shorter than 5 characters is rejected."""
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Bad',
        'category': 'Wet',
        'location': 'Local Market',
        'description': 'Valid long description of waste hotspot.'
    }, follow_redirects=True)

    assert b"Title must be between 5 and 150 characters" in response.data


def test_short_description_rejected(auth_citizen_client):
    """Description shorter than 10 characters is rejected."""
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Valid Title Hotspot',
        'category': 'Wet',
        'location': 'Local Market',
        'description': 'Too short'
    }, follow_redirects=True)

    assert b"Please provide a detailed description" in response.data


def test_invalid_coordinate_bounds_rejected(auth_citizen_client):
    """Coordinates outside physical latitude/longitude ranges are rejected."""
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Out of Bounds Hotspot',
        'category': 'Dry',
        'location': 'Antarctica Edge',
        'latitude': '999.99',
        'longitude': '72.84',
        'description': 'Valid description with corrupt latitude coordinates.'
    }, follow_redirects=True)

    assert b"Geographic coordinates are out of valid bounds" in response.data


def test_disallowed_file_extension_rejected(auth_citizen_client):
    """Uploading an executable script disguised as a photo is rejected."""
    fake_script = io.BytesIO(b"print('malicious script')")
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Malicious Upload Test',
        'category': 'Dry',
        'location': 'Cyber Cafe',
        'description': 'Valid description testing file extension whitelist.',
        'photo': (fake_script, 'exploit.py')
    }, follow_redirects=True)

    assert b"Invalid file type" in response.data


def test_fake_image_binary_rejected(auth_citizen_client):
    """Uploading random text with a .jpg extension fails Pillow binary verification."""
    fake_image = io.BytesIO(b"Not an actual JPEG image stream header")
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Corrupted Image Test',
        'category': 'Plastic',
        'location': 'Testing Lab',
        'description': 'Valid description testing image binary integrity.',
        'photo': (fake_image, 'corrupted.jpg')
    }, follow_redirects=True)

    assert b"Uploaded file is corrupted or not a valid image" in response.data


def test_path_traversal_image_serving(client):
    """Path traversal attempt on uploads endpoint must be blocked."""
    response = client.get('/uploads/reports/../../config.py')
    assert response.status_code in (403, 404)


def test_api_reports_filtering(client, app, sample_users):
    """API endpoint returns only geo-located reports and filters properly by category."""
    with app.app_context():
        r1 = Report(
            user_id=sample_users['citizen'].id,
            title="Plastic in Colaba",
            category="Plastic",
            location="Colaba Causeway",
            latitude=18.9220,
            longitude=72.8315,
            description="Discarded plastic bags.",
            status="Reported"
        )
        r2 = Report(
            user_id=sample_users['citizen'].id,
            title="E-waste in Dadar",
            category="E-waste",
            location="Dadar West",
            latitude=19.0178,
            longitude=72.8478,
            description="Broken motherboards.",
            status="In Progress"
        )
        # Report without coordinates
        r3 = Report(
            user_id=sample_users['citizen'].id,
            title="No Coords Dry Waste",
            category="Dry",
            location="Bandra",
            latitude=None,
            longitude=None,
            description="No coords.",
            status="Reported"
        )
        db.session.add_all([r1, r2, r3])
        db.session.commit()

    # Query all geo reports
    res_all = client.get('/api/reports')
    data_all = res_all.get_json()
    assert data_all['count'] == 2  # Only r1 and r2 have coordinates!

    # Query filtered by category Plastic
    res_plastic = client.get('/api/reports?category=Plastic')
    data_plastic = res_plastic.get_json()
    assert data_plastic['count'] == 1
    assert data_plastic['reports'][0]['title'] == 'Plastic in Colaba'

