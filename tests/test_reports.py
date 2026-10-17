"""
Automated tests for waste reporting, filtering, and report lifecycle management.
"""
import os
from models import db, Report



def test_create_report_with_coordinates(auth_citizen_client, app, sample_users):
    """Test reporting a waste hotspot with valid coordinates."""
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Plastic bottles on Shivaji Park Beach',
        'category': 'Plastic',
        'location': 'Shivaji Park Promenade, Dadar West',
        'latitude': '19.0269',
        'longitude': '72.8373',
        'description': 'Piles of beverage containers and food packets accumulating near the sea wall.'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        report = Report.query.filter_by(title='Plastic bottles on Shivaji Park Beach').first()
        assert report is not None
        assert report.category == 'Plastic'
        assert report.latitude == 19.0269
        assert report.longitude == 72.8373
        assert report.status == 'Reported'
        assert report.has_coordinates is True
        assert report.user_id == sample_users['citizen'].id


def test_create_report_without_coordinates(auth_citizen_client, app):
    """Test reporting a waste hotspot with missing coordinates (graceful handling)."""
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Vegetable compost dumped near municipal market',
        'category': 'Wet',
        'location': 'Near Flower Market, Dadar Station Road',
        'latitude': '',
        'longitude': '',
        'description': 'Rotting vegetable residue dumped in open bins without segregation.'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        report = Report.query.filter_by(title='Vegetable compost dumped near municipal market').first()
        assert report is not None
        assert report.latitude is None
        assert report.longitude is None
        assert report.has_coordinates is False


def test_create_report_with_photo(auth_citizen_client, app, dummy_image):
    """Test reporting waste hotspot with an optional valid image attachment."""
    response = auth_citizen_client.post('/report', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Electronic waste cables on link road',
        'category': 'E-waste',
        'location': 'New Link Road, Andheri West',
        'description': 'Discarded wiring, power adapters, and monitors piled on sidewalk.',
        'photo': (dummy_image, 'evidence.png')
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        report = Report.query.filter_by(title='Electronic waste cables on link road').first()
        assert report is not None
        assert report.image_filename is not None
        assert report.image_filename.endswith('.png')


def test_unauthenticated_user_cannot_report(client):
    """Ensure guests cannot submit reports and are redirected to login."""
    response = client.get('/report', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_citizen_can_edit_own_pending_report(auth_citizen_client, app, sample_users):
    """Citizen can edit their report when status is still 'Reported'."""
    with app.app_context():
        report = Report(
            user_id=sample_users['citizen'].id,
            title="Original Title Pending",
            category="Dry",
            location="Original Location",
            description="Initial description of cardboard boxes."
        )
        db.session.add(report)
        db.session.commit()
        report_id = report.id

    response = auth_citizen_client.post(f'/reports/{report_id}/edit', data={
        'csrf_token': 'test-valid-csrf-token',
        'title': 'Updated Title for Cardboard Waste',
        'category': 'Dry',
        'location': 'Updated Location at Ranade Road',
        'description': 'Updated detailed description about dry paper packaging.'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        updated = db.session.get(Report, report_id)
        assert updated.title == 'Updated Title for Cardboard Waste'
        assert updated.location == 'Updated Location at Ranade Road'


def test_citizen_cannot_edit_inprogress_report(auth_citizen_client, app, sample_users):
    """Citizen cannot edit a report that has transitioned to 'In Progress'."""
    with app.app_context():
        report = Report(
            user_id=sample_users['citizen'].id,
            title="In Progress Report",
            category="Dry",
            location="Some Location",
            description="Sanitation crew already assigned.",
            status="In Progress"
        )
        db.session.add(report)
        db.session.commit()
        report_id = report.id

    response = auth_citizen_client.get(f'/reports/{report_id}/edit', follow_redirects=True)
    assert b"Reports that are In Progress or Resolved can no longer be edited" in response.data


def test_unauthorized_citizen_cannot_edit_others_report(client, app, sample_users):
    """Citizen B cannot edit Citizen A's report."""
    with app.app_context():
        report = Report(
            user_id=sample_users['citizen'].id,
            title="Citizen A Report",
            category="Dry",
            location="Citizen A Landmark",
            description="Citizen A description."
        )
        db.session.add(report)
        db.session.commit()
        report_id = report.id

    # Authenticate as Citizen 2 (different user)
    with client.session_transaction() as sess:
        sess['user_id'] = sample_users['citizen2'].id
        sess['user_role'] = 'citizen'
        sess['_csrf_token'] = 'token'

    response = client.get(f'/reports/{report_id}/edit')
    assert response.status_code == 403


def test_category_fallback_images_and_rendering(auth_citizen_client, app, sample_users):
    """Test image display and category fallbacks for reports with and without photos."""
    with app.app_context():
        # Create report without photo
        report_no_photo = Report(
            user_id=sample_users['citizen'].id,
            title="Organic vegetable waste corner",
            category="Wet",
            location="Market Lane",
            description="Decomposing wet waste requiring municipal clearance."
        )
        db.session.add(report_no_photo)
        db.session.commit()
        no_photo_id = report_no_photo.id

        # Verify model sample photo and fallback properties
        assert report_no_photo.category_slug == 'wet'
        assert report_no_photo.fallback_image_url == '/static/images/fallbacks/wet.svg'
        assert report_no_photo.has_valid_image is False
        assert report_no_photo.sample_photo_filename == 'wet_organic_waste.jpg'
        assert report_no_photo.display_image_url == '/static/images/photos/wet_organic_waste.jpg'

        # Verify photo and fallback SVG files physically exist on disk
        photo_path = os.path.join(app.root_path, 'static', 'images', 'photos', 'wet_organic_waste.jpg')
        assert os.path.isfile(photo_path)
        svg_path = os.path.join(app.root_path, 'static', 'images', 'fallbacks', 'wet.svg')
        assert os.path.isfile(svg_path)

    # Test report detail page displays sample photo and no 'No photo attached' placeholder
    detail_resp = auth_citizen_client.get(f'/reports/{no_photo_id}')
    assert detail_resp.status_code == 200
    assert b'No photo attached' not in detail_resp.data
    assert b'wet_organic_waste.jpg' in detail_resp.data
    assert b'/static/images/fallbacks/wet.svg' in detail_resp.data

    # Test my-reports table page displays sample photo thumbnail
    my_resp = auth_citizen_client.get('/my-reports')
    assert my_resp.status_code == 200
    assert b'No photo attached' not in my_resp.data
    assert b'wet_organic_waste.jpg' in my_resp.data

