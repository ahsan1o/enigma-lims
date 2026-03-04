"""
Database Models for Kotli LIMS
SQLAlchemy ORM models for all core entities
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class Patient(Base):
    """Patient Information"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("Male", "Female", "Other"), nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    doctor = relationship("Doctor", back_populates="patients")
    samples = relationship("Sample", back_populates="patient")


class Doctor(Base):
    """Doctor Information"""
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    registration_number = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    clinic_name = Column(String(255))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patients = relationship("Patient", back_populates="doctor")
    orders = relationship("Order", back_populates="doctor")


class Sample(Base):
    """Sample Information"""
    __tablename__ = "samples"
    
    id = Column(Integer, primary_key=True)
    sample_id = Column(String(50), unique=True, nullable=False)  # Barcode
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    sample_type = Column(String(100), nullable=False)  # Blood, Urine, etc
    collection_date = Column(DateTime, nullable=False)
    collection_time = Column(String(10))
    received_date = Column(DateTime)
    status = Column(String(50), default="pending")  # pending, testing, completed, approved
    notes = Column(Text)
    priority = Column(String(20), default="routine")  # routine, urgent, stat
    rejection_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="samples")
    orders = relationship("Order", back_populates="sample")
    results = relationship("Result", back_populates="sample")


class Test(Base):
    """Test Definition"""
    __tablename__ = "tests"
    
    id = Column(Integer, primary_key=True)
    test_code = Column(String(50), unique=True, nullable=False)
    test_name = Column(String(255), nullable=False)
    description = Column(Text)
    unit = Column(String(50))
    reference_min = Column(Float)
    reference_max = Column(Float)
    critical_min = Column(Float)
    critical_max = Column(Float)
    method = Column(String(255))
    machine_id = Column(Integer, ForeignKey("instruments.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    instrument = relationship("Instrument", back_populates="tests")
    orders = relationship("Order", back_populates="test")
    results = relationship("Result", back_populates="test")


class Order(Base):
    """Test Order"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    priority = Column(String(20), default="normal")  # normal, urgent, stat
    status = Column(String(50), default="pending")  # pending, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sample = relationship("Sample", back_populates="orders")
    test = relationship("Test", back_populates="orders")
    doctor = relationship("Doctor", back_populates="orders")
    results = relationship("Result", back_populates="order")


class Result(Base):
    """Test Result"""
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    result_value = Column(String(50), nullable=False)
    unit = Column(String(50))
    status = Column(String(50), default="normal")  # normal, abnormal, critical
    qc_passed = Column(Boolean, default=True)
    interpretation = Column(Text)
    entered_by = Column(Integer, ForeignKey("users.id"))  # Technician
    entered_date = Column(DateTime)
    approved_by = Column(Integer, ForeignKey("users.id"))  # Supervisor
    approved_date = Column(DateTime)
    machine_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="results")
    sample = relationship("Sample", back_populates="results")
    test = relationship("Test", back_populates="results")
    entered_by_user = relationship("User", foreign_keys=[entered_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])


class User(Base):
    """User Account"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    role = Column(String(50), nullable=False)  # admin, technician, supervisor, doctor
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user")


class Instrument(Base):
    """Lab Instrument/Machine"""
    __tablename__ = "instruments"
    
    id = Column(Integer, primary_key=True)
    instrument_code = Column(String(50), unique=True, nullable=False)
    instrument_name = Column(String(255), nullable=False)
    manufacturer = Column(String(255))
    model = Column(String(100))
    location = Column(String(255))
    serial_number = Column(String(100))
    last_calibration = Column(DateTime)
    next_calibration = Column(DateTime)
    status = Column(String(50), default="active")  # active, inactive, maintenance
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tests = relationship("Test", back_populates="instrument")


class AuditLog(Base):
    """Audit Trail for Compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255), nullable=False)
    table_name = Column(String(100))
    record_id = Column(Integer)
    old_value = Column(Text)
    new_value = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")


class SyncQueue(Base):
    """Queue for Offline Sync"""
    __tablename__ = "sync_queue"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String(50), nullable=False)  # sample, result, user, etc
    entity_id = Column(Integer)
    action = Column(String(50), nullable=False)  # create, update, delete
    data = Column(Text)  # JSON
    synced = Column(Boolean, default=False)
    synced_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    retry_count = Column(Integer, default=0)
    last_error = Column(Text)


class TestPanel(Base):
    """Test Panel / Profile — bundles multiple tests for quick ordering"""
    __tablename__ = "test_panels"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    panel_items = relationship("TestPanelItem", back_populates="panel", cascade="all, delete-orphan")


class TestPanelItem(Base):
    """Tests within a Panel"""
    __tablename__ = "test_panel_items"

    id = Column(Integer, primary_key=True)
    panel_id = Column(Integer, ForeignKey("test_panels.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)

    panel = relationship("TestPanel", back_populates="panel_items")
    test = relationship("Test")


class Invoice(Base):
    """Patient Invoice / Bill"""
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"))
    total_amount = Column(Float, default=0.0)
    paid_amount = Column(Float, default=0.0)
    status = Column(String(20), default="unpaid")  # unpaid, partial, paid
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship("Patient")
    sample = relationship("Sample")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    """Line items on an Invoice"""
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    description = Column(String(255), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"))
    amount = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    test = relationship("Test")


class Reagent(Base):
    """Reagent / Consumable Inventory"""
    __tablename__ = "reagents"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    catalog_number = Column(String(100))
    current_stock = Column(Float, default=0.0)
    min_stock_level = Column(Float, default=0.0)
    unit = Column(String(50))  # boxes, kits, mL, etc.
    expiry_date = Column(DateTime)
    supplier = Column(String(255))
    instrument_id = Column(Integer, ForeignKey("instruments.id"))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    instrument = relationship("Instrument")
