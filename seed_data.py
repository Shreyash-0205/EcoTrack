"""
Sample seed data generator for EcoTrack demonstration.
Populates realistic demo reports for Mumbai metropolitan civic areas.
All sample reports are explicitly tagged with is_demo=True and a demo identifier.
"""
import os
import secrets
from datetime import datetime, timezone, timedelta
from app import create_app
from models import db, User, Report, ActivityLog


def seed_database():
    """Seed the database with initial users, demo reports, and audit logs."""
    app = create_app('development')
    with app.app_context():
        # Clean slate or re-seed
        print("[EcoTrack Seed] Initializing database tables...")
        db.create_all()

        # Check if already seeded
        if User.query.filter_by(email='admin@ecotrack.org').first():
            print("[EcoTrack Seed] Database is already populated. Skipping duplicate seeding.")
            return

        print("[EcoTrack Seed] Creating demo users...")
        # Resolve initial passwords safely without hardcoding in published source:
        # Check environment variables first (ECOTRACK_ADMIN_PASSWORD, ECOTRACK_CITIZEN_PASSWORD).
        # If not set, generate cryptographically secure random passwords for this local installation.
        admin_password = os.environ.get('ECOTRACK_ADMIN_PASSWORD')
        admin_pw_generated = False
        if not admin_password:
            admin_password = secrets.token_urlsafe(12)
            admin_pw_generated = True

        citizen_password = os.environ.get('ECOTRACK_CITIZEN_PASSWORD')
        citizen_pw_generated = False
        if not citizen_password:
            citizen_password = secrets.token_urlsafe(12)
            citizen_pw_generated = True

        # 1. Administrator
        admin = User(
            name="Civic Administrator (MCGM)",
            email="admin@ecotrack.org",
            role="admin"
        )
        admin.set_password(admin_password)
        db.session.add(admin)

        # 2. Citizens
        citizen1 = User(
            name="Aarav Sharma",
            email="citizen@ecotrack.org",
            role="citizen"
        )
        citizen1.set_password(citizen_password)
        db.session.add(citizen1)

        citizen2 = User(
            name="Priya Deshmukh",
            email="priya@ecotrack.org",
            role="citizen"
        )
        citizen2.set_password(citizen_password)
        db.session.add(citizen2)

        citizen3 = User(
            name="Rohan Kulkarni",
            email="rohan@ecotrack.org",
            role="citizen"
        )
        citizen3.set_password(citizen_password)
        db.session.add(citizen3)

        db.session.commit()

        print("[EcoTrack Seed] Creating realistic Mumbai civic demo reports...")
        now = datetime.now(timezone.utc)

        sample_reports = [
            {
                'user_id': citizen1.id,
                'title': "[DEMO] Overflowing Dry Waste Bins near Dadar Station West",
                'description': "Large accumulation of cardboard cartons, paper packaging, and empty beverage containers obstructing pedestrian footpath near Dadar West railway station exit.",
                'category': 'Dry',
                'location': "Ranade Road, Near Dadar Railway Station (West), Mumbai 400028",
                'latitude': 19.0178,
                'longitude': 72.8478,
                'status': 'Reported',
                'admin_notes': None,
                'created_at': now - timedelta(days=2, hours=4),
                'is_demo': True
            },
            {
                'user_id': citizen2.id,
                'title': "[DEMO] Single-Use Plastic Waste near Juhu Beach Promenade",
                'description': "Piles of discarded plastic bottles, food wrappers, and polyethene carry bags accumulated on the beach pathway following weekend evening crowds.",
                'category': 'Plastic',
                'location': "Juhu Tara Road, Juhu Beach North Entry, Mumbai 400049",
                'latitude': 19.0988,
                'longitude': 72.8264,
                'status': 'In Progress',
                'admin_notes': "Assigned to Ward K/West cleanup crew. Mechanical sweeping scheduled for 7:00 AM.",
                'created_at': now - timedelta(days=3, hours=10),
                'is_demo': True
            },
            {
                'user_id': citizen1.id,
                'title': "[DEMO] Decomposed Wet Vegetable Waste Dumped near APMC Market Vashi",
                'description': "Rotting organic matter and vegetable trimmings dumped along service road creating foul odor and pest infestation.",
                'category': 'Wet',
                'location': "Sector 19, APMC Market Outer Ring Road, Vashi, Navi Mumbai 400705",
                'latitude': 19.0736,
                'longitude': 73.0031,
                'status': 'Resolved',
                'admin_notes': "Wet waste collected by organic composting mobile unit. Area sanitized with lime powder.",
                'created_at': now - timedelta(days=5, hours=2),
                'is_demo': True
            },
            {
                'user_id': citizen3.id,
                'title': "[DEMO] Discarded Computer Monitors and CRT Glass near Lamington Road",
                'description': "Dangerous electronic waste including broken computer monitors, circuit boards, and cables placed beside electrical junction box.",
                'category': 'E-waste',
                'location': "Dr. Dadasaheb Bhadkamkar Marg (Lamington Road), Grant Road, Mumbai 400007",
                'latitude': 18.9633,
                'longitude': 72.8172,
                'status': 'In Progress',
                'admin_notes': "Dispatched authorized MPCB registered e-waste recycler team for safe dismantling and transport.",
                'created_at': now - timedelta(days=1, hours=8),
                'is_demo': True
            },
            {
                'user_id': citizen2.id,
                'title': "[DEMO] Unsegregated Mixed Garbage Dump beside Bandra Kurla Complex Road",
                'description': "Substantial dump containing combined food waste, plastic cutlery, and thermocol packaging causing street clutter.",
                'category': 'Mixed',
                'location': "BKC Connector Junction, G Block, Bandra Kurla Complex, Mumbai 400051",
                'latitude': 19.0657,
                'longitude': 72.8688,
                'status': 'Reported',
                'admin_notes': None,
                'created_at': now - timedelta(hours=14),
                'is_demo': True
            },
            {
                'user_id': citizen1.id,
                'title': "[DEMO] Construction Debris and Mixed Rubble on Link Road Andheri",
                'description': "Broken tiles, concrete chunks, and plaster bags left unattended near the metro pillar.",
                'category': 'Other',
                'location': "New Link Road, Near Infiniti Mall, Andheri West, Mumbai 400053",
                'latitude': 19.1415,
                'longitude': 72.8317,
                'status': 'Reported',
                'admin_notes': None,
                'created_at': now - timedelta(days=4),
                'is_demo': True
            },
            {
                'user_id': citizen3.id,
                'title': "[DEMO] Organic Kitchen Waste and Garden Clippings near Shivaji Park",
                'description': "Trimmed tree branches, leaves, and compostable kitchen waste piled along perimeter walkway.",
                'category': 'Wet',
                'location': "Cadell Road, Shivaji Park Outer Ring, Dadar, Mumbai 400028",
                'latitude': 19.0269,
                'longitude': 72.8373,
                'status': 'Resolved',
                'admin_notes': "Processed on-site by community vermicomposting team.",
                'created_at': now - timedelta(days=7),
                'is_demo': True
            },
            {
                'user_id': citizen2.id,
                'title': "[DEMO] Discarded Plastic Mineral Water Bottles at Marine Drive Promenade",
                'description': "Tetra paks and plastic bottles caught between tetrapods along the sea wall.",
                'category': 'Plastic',
                'location': "Netaji Subhash Chandra Bose Road (Marine Drive), Nariman Point, Mumbai 400021",
                'latitude': 18.9242,
                'longitude': 72.8228,
                'status': 'Resolved',
                'admin_notes': "Special coastal cleanup volunteer drive completed with Municipal Corporation.",
                'created_at': now - timedelta(days=6),
                'is_demo': True
            },
            # Reports without coordinates to demonstrate graceful handling of missing coordinates
            {
                'user_id': citizen1.id,
                'title': "[DEMO] Old Rechargeable Batteries Dumped Behind Station Society",
                'description': "Multiple lead-acid and lithium rechargeable cells disposed behind the residential building without segregation.",
                'category': 'E-waste',
                'location': "Station Road, Near Sahakari Bhandar, Mulund West, Mumbai",
                'latitude': None,
                'longitude': None,
                'status': 'Reported',
                'admin_notes': "Awaiting precise GPS verification from reporter.",
                'created_at': now - timedelta(hours=6),
                'is_demo': True
            },
            {
                'user_id': citizen2.id,
                'title': "[DEMO] Mixed Waste Piles near Ghatkopar East Market",
                'description': "Assorted vegetable peels, cardboard, and polythene dumped near community dustbin.",
                'category': 'Mixed',
                'location': "MG Road, Behind Municipal Hospital, Ghatkopar East, Mumbai",
                'latitude': None,
                'longitude': None,
                'status': 'In Progress',
                'admin_notes': "Sanitation inspector deputed for physical verification.",
                'created_at': now - timedelta(days=2),
                'is_demo': True
            }
        ]

        created_reports = []
        for rep_data in sample_reports:
            rep = Report(**rep_data)
            db.session.add(rep)
            created_reports.append(rep)

        db.session.commit()

        print("[EcoTrack Seed] Generating realistic administrative activity logs...")
        logs = [
            ActivityLog(
                admin_user_id=admin.id,
                report_id=created_reports[1].id,
                action="Status updated from 'Reported' to 'In Progress'",
                details="Assigned to Ward K/West cleanup crew. Mechanical sweeping scheduled for 7:00 AM.",
                created_at=now - timedelta(days=2, hours=12)
            ),
            ActivityLog(
                admin_user_id=admin.id,
                report_id=created_reports[2].id,
                action="Status updated from 'Reported' to 'Resolved'",
                details="Wet waste collected by organic composting mobile unit. Area sanitized with lime powder.",
                created_at=now - timedelta(days=4, hours=6)
            ),
            ActivityLog(
                admin_user_id=admin.id,
                report_id=created_reports[3].id,
                action="Status updated from 'Reported' to 'In Progress'",
                details="Dispatched authorized MPCB registered e-waste recycler team.",
                created_at=now - timedelta(hours=20)
            ),
            ActivityLog(
                admin_user_id=admin.id,
                report_id=created_reports[6].id,
                action="Status updated from 'Reported' to 'Resolved'",
                details="Processed on-site by community vermicomposting team.",
                created_at=now - timedelta(days=6, hours=1)
            ),
            ActivityLog(
                admin_user_id=admin.id,
                report_id=created_reports[7].id,
                action="Status updated from 'Reported' to 'Resolved'",
                details="Special coastal cleanup volunteer drive completed with Municipal Corporation.",
                created_at=now - timedelta(days=5, hours=18)
            ),
            ActivityLog(
                admin_user_id=admin.id,
                report_id=created_reports[9].id,
                action="Status updated from 'Reported' to 'In Progress'",
                details="Sanitation inspector deputed for physical verification.",
                created_at=now - timedelta(days=1, hours=2)
            )
        ]

        for log in logs:
            db.session.add(log)

        print("[EcoTrack Seed] Database seeded successfully!")
        print(f"  - Admin user: {admin.email}")
        if admin_pw_generated:
            print(f"    Generated password: {admin_password}")
            print("    (Set ECOTRACK_ADMIN_PASSWORD env var to customize)")
        else:
            print("    Password: configured via ECOTRACK_ADMIN_PASSWORD")

        print(f"  - Citizen user: {citizen1.email}")
        if citizen_pw_generated:
            print(f"    Generated password: {citizen_password}")
            print("    (Set ECOTRACK_CITIZEN_PASSWORD env var to customize)")
        else:
            print("    Password: configured via ECOTRACK_CITIZEN_PASSWORD")

        print(f"  - Total sample reports created: {len(sample_reports)}")


if __name__ == '__main__':
    seed_database()

