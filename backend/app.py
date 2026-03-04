"""
Kotli LIMS - Main FastAPI Application
Offline-capable Clinical Laboratory Information Management System
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from database import init_db, get_db, create_default_admin
from models import User
from utils.auth import verify_token

# Import and include all API routers
from api.auth import router as auth_router
from api.patients import router as patients_router
from api.doctors import router as doctors_router
from api.samples import router as samples_router
from api.tests import router as tests_router
from api.orders import router as orders_router
from api.results import router as results_router
from api.instruments import router as instruments_router
from api.users import router as users_router
from api.dashboard import router as dashboard_router
from api.reports import router as reports_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Kotli LIMS",
    description="Offline-Capable Clinical Laboratory Information Management System",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routers
app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(samples_router)
app.include_router(tests_router)
app.include_router(orders_router)
app.include_router(results_router)
app.include_router(instruments_router)
app.include_router(users_router)
app.include_router(dashboard_router)
app.include_router(reports_router)


# ============================================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
def startup_event():
    """Initialize database and default data on startup"""
    logger.info("Kotli LIMS Starting...")
    init_db()
    create_default_admin()
    logger.info("Initialization complete")


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Kotli LIMS Shutting down...")


# ============================================================================
# AUTHENTICATION DEPENDENCY
# ============================================================================

async def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Kotli LIMS",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@app.get("/api/info")
def get_info():
    """Get system information"""
    return {
        "name": "Kotli LIMS",
        "version": "1.0.0",
        "description": "Offline-Capable Clinical Laboratory Information Management System",
        "capabilities": [
            "Sample Management",
            "Test Ordering",
            "Machine Integration",
            "Results Management",
            "Report Generation",
            "User Authentication",
            "Offline Sync",
            "Audit Logging"
        ],
        "mode": "OFFLINE_ENABLED"
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status": "error"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status": "error"}
    )


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/api")
def root():
    """Root API endpoint"""
    return {
        "message": "Welcome to Kotli LIMS",
        "docs": "/api/docs",
        "health": "/api/health",
        "info": "/api/info"
    }


# ============================================================================
# STATIC FILE SERVING — Offline EXE mode
# Set LIMS_FRONTEND_DIR env var to enable (done by launcher.py)
# ============================================================================

import os as _os
_frontend_dir = _os.environ.get('LIMS_FRONTEND_DIR')
if _frontend_dir and _os.path.exists(_frontend_dir):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="static")
    logger.info(f"Serving frontend from: {_frontend_dir}")


# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                    KOTLI LIMS SERVER                           ║
    ║        Offline-Capable Laboratory Information System           ║
    ║                                                                ║
    ║  Starting on http://127.0.0.1:8000                            ║
    ║  API Documentation: http://127.0.0.1:8000/api/docs            ║
    ║                                                                ║
    ║  Default Login: admin / admin123                              ║
    ║  Change password after first login!                            ║
    ╚════════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
