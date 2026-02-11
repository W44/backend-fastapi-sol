"""
Seed script to populate the database with sample seashell data.
Run this after starting the database to add test data.

This script connects to the LOCAL Docker Compose database.
"""
import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Parse command line arguments
parser = argparse.ArgumentParser(description='Seed database with sample data')
parser.add_argument('--username', default='seashell_user', help='Database username')
parser.add_argument('--password', default='seashell_password', help='Database password')
args = parser.parse_args()

# Override DATABASE_URL to use local Docker database
os.environ["DATABASE_URL"] = f"postgresql://{args.username}:{args.password}@localhost:5432/seashell_db"


from sqlmodel import Session, select 
from app.db.session import engine, init_db 
from app.models.seashell import Seashell 


# Sample seashell data
SAMPLE_SEASHELLS = [
    {
        "name": "Queen Conch",
        "species": "Strombus gigas",
        "description": "Large tropical sea snail with beautiful pink interior"
    },
    {
        "name": "Tiger Cowrie",
        "species": "Cypraea tigris",
        "description": "Glossy shell with distinctive tiger-like spots"
    },
    {
        "name": "Nautilus",
        "species": "Nautilus pompilius",
        "description": "Ancient mollusk with chambered spiral shell"
    },
    {
        "name": "Scallop",
        "species": "Pecten maximus",
        "description": "Fan-shaped shell with radiating ribs"
    },
    {
        "name": "Abalone",
        "species": "Haliotis rufescens",
        "description": "Ear-shaped shell with iridescent interior"
    },
    {
        "name": "Murex",
        "species": "Murex pecten",
        "description": "Spiny shell historically used for purple dye"
    },
    {
        "name": "Cone Shell",
        "species": "Conus textile",
        "description": "Beautifully patterned but venomous sea snail"
    },
    {
        "name": "Triton's Trumpet",
        "species": "Charonia tritonis",
        "description": "Large shell used as musical instrument"
    }
]


def seed_database():
    """Insert sample seashell data into the database"""
    print("Starting database seed...")
    
    # Ensure tables exist
    print("Initializing database tables...")
    init_db()
    
    with Session(engine) as session:
        # Check if data already exists
        statement = select(Seashell)
        existing_shells = session.exec(statement).all()
        existing_count = len(existing_shells)
        
        if existing_count > 0:
            print(f"Database already has {existing_count} seashells")
            response = input("Do you want to add more sample data anyway? (y/n): ")
            if response.lower() != 'y':
                print("Seed cancelled")
                return
        
        # Insert sample data
        for shell_data in SAMPLE_SEASHELLS:
            seashell = Seashell(**shell_data)
            session.add(seashell)
        
        session.commit()
        print(f"Successfully added {len(SAMPLE_SEASHELLS)} seashells to the database!")
        print("\nSample data:")
        for shell in SAMPLE_SEASHELLS:
            print(f"  - {shell['name']} ({shell['species']})")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)
