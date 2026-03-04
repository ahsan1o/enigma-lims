"""
Database Configuration and Session Management
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from models import Base

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DB_PATH, exist_ok=True)

DB_URL = f"sqlite:///{os.path.join(DB_PATH, 'kotli_lims.db')}"

# Create SQLite engine with check_same_thread=False to allow multi-threaded access
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _migrate_schema():
    """Run safe schema migrations for columns added after initial release."""
    migrations = [
        "ALTER TABLE tests ADD COLUMN price FLOAT DEFAULT 0.0",
    ]
    with engine.connect() as conn:
        for sql in migrations:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception:
                pass  # Column already exists — safe to ignore


def init_db():
    """Initialize database with all tables"""
    Base.metadata.create_all(bind=engine)
    _migrate_schema()
    print(f"✅ Database initialized at {DB_URL}")


def get_db() -> Session:
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create default admin user on first run
def create_default_admin():
    """Create default admin user if database is empty"""
    from sqlalchemy import func
    from models import User
    from utils.auth import hash_password

    db = SessionLocal()
    try:
        user_count = db.query(func.count(User.id)).scalar()
        if user_count == 0:
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                full_name="System Administrator",
                email="admin@kotli-lims.local",
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✅ Default admin user created (username: admin, password: admin123)")
            print("⚠️  IMPORTANT: Change password immediately after first login!")
    finally:
        db.close()


def create_default_technician():
    """Create default lab technician user if it does not exist yet."""
    from models import User
    from utils.auth import hash_password

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "tech").first()
        if not existing:
            tech = User(
                username="tech",
                password_hash=hash_password("tech123"),
                full_name="Lab Technician",
                email="tech@kotli-lims.local",
                role="technician",
                is_active=True
            )
            db.add(tech)
            db.commit()
            print("✅ Default technician user created (username: tech, password: tech123)")
    finally:
        db.close()
