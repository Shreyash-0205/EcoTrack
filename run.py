"""
Convenience launcher for EcoTrack web application.
Checks database existence, runs seeder if needed, and launches the server.
"""
import os
from pathlib import Path
from app import create_app
from seed_data import seed_database
from models import db, User

if __name__ == '__main__':
    db_file = Path(__file__).resolve().parent / 'ecotrack.db'
    if not db_file.exists():
        print("[EcoTrack] Initializing and seeding demo database...")
        seed_database()

    app = create_app('development')

    print("=" * 65)
    print(" EcoTrack — Smart Waste Management & Segregation System")
    print(" University of Mumbai — B.E. Open Source Engineering Project")
    print("=" * 65)
    print(" Server running at: http://127.0.0.1:5000")
    print("-" * 65)
    print(" Local Demonstration Accounts (initialized via seed_data.py):")
    print("   • Administrator: admin@ecotrack.org")
    print("   • Citizen:       citizen@ecotrack.org")
    print("   • Citizen 2:     priya@ecotrack.org")
    print("   (Local credentials managed via environment variables or seed_data.py)")
    print("=" * 65)

    app.run(host='127.0.0.1', port=5000, debug=True)

