from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime

# Auth
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# User schemas
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str  # admin, technician, supervisor, doctor

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    role: str
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    class Config:
        from_attributes = True

# Patient schemas
class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str  # Male, Female, Other
    phone: Optional[str] = None
    email: Optional[str] = None
    doctor_id: Optional[int] = None
    referring_doctor_name: Optional[str] = None

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, v):
        if v:
            return v.capitalize()
        return v

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    doctor_id: Optional[int] = None
    referring_doctor_name: Optional[str] = None

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, v):
        if v:
            return v.capitalize()
        return v

class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    phone: Optional[str]
    email: Optional[str]
    doctor_id: Optional[int]
    doctor_name: Optional[str] = None
    referring_doctor_name: Optional[str] = None
    created_at: datetime

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, v):
        if v:
            return v.capitalize()
        return v

    class Config:
        from_attributes = True

# Doctor schemas
class DoctorCreate(BaseModel):
    name: str
    registration_number: str
    phone: Optional[str] = None
    email: Optional[str] = None
    clinic_name: Optional[str] = None
    address: Optional[str] = None

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    clinic_name: Optional[str] = None
    address: Optional[str] = None

class DoctorResponse(BaseModel):
    id: int
    name: str
    registration_number: str
    phone: Optional[str]
    email: Optional[str]
    clinic_name: Optional[str]
    address: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# Sample schemas
class SampleCreate(BaseModel):
    patient_id: int
    sample_type: str  # Blood, Urine, Stool, etc.
    collection_date: datetime
    collection_time: Optional[str] = None
    notes: Optional[str] = None
    priority: str = "routine"  # routine, urgent, stat

class SampleStatusUpdate(BaseModel):
    status: str  # pending, testing, completed, approved

class SampleReject(BaseModel):
    rejection_reason: str

class SampleResponse(BaseModel):
    id: int
    sample_id: str
    patient_id: int
    patient_name: Optional[str] = None
    sample_type: str
    collection_date: datetime
    collection_time: Optional[str]
    received_date: Optional[datetime]
    status: str
    priority: Optional[str] = "routine"
    rejection_reason: Optional[str] = None
    notes: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# Test schemas
class TestCreate(BaseModel):
    test_code: str
    test_name: str
    description: Optional[str] = None
    unit: Optional[str] = None
    reference_min: Optional[float] = None
    reference_max: Optional[float] = None
    critical_min: Optional[float] = None
    critical_max: Optional[float] = None
    price: Optional[float] = 0.0
    method: Optional[str] = None
    machine_id: Optional[int] = None

class TestUpdate(BaseModel):
    test_name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    reference_min: Optional[float] = None
    reference_max: Optional[float] = None
    critical_min: Optional[float] = None
    critical_max: Optional[float] = None
    price: Optional[float] = None
    method: Optional[str] = None

class TestResponse(BaseModel):
    id: int
    test_code: str
    test_name: str
    description: Optional[str]
    unit: Optional[str]
    reference_min: Optional[float]
    reference_max: Optional[float]
    critical_min: Optional[float]
    critical_max: Optional[float]
    price: Optional[float] = 0.0
    method: Optional[str]
    machine_id: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True

# Order schemas
class OrderCreate(BaseModel):
    sample_id: int
    test_id: int
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    priority: str = "normal"  # normal, urgent, stat

class OrderResponse(BaseModel):
    id: int
    sample_id: int
    test_id: int
    doctor_id: Optional[int] = None
    patient_name: Optional[str] = None
    test_name: Optional[str] = None
    test_code: Optional[str] = None
    test_price: Optional[float] = None
    sample_barcode: Optional[str] = None
    doctor_name: Optional[str] = None
    priority: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# Result schemas
class ResultCreate(BaseModel):
    order_id: int
    sample_id: int
    test_id: int
    result_value: str
    unit: Optional[str] = None
    interpretation: Optional[str] = None

class ResultApprove(BaseModel):
    comments: Optional[str] = None

class ResultResponse(BaseModel):
    id: int
    order_id: int
    sample_id: int
    test_id: int
    test_name: Optional[str] = None
    test_code: Optional[str] = None
    result_value: str
    unit: Optional[str]
    status: str
    qc_passed: bool
    interpretation: Optional[str]
    entered_by: Optional[int]
    entered_by_name: Optional[str] = None
    entered_date: Optional[datetime]
    approved_by: Optional[int]
    approved_by_name: Optional[str] = None
    approved_date: Optional[datetime]
    machine_generated: bool
    created_at: datetime
    price: Optional[float] = None
    reference_min: Optional[float] = None
    reference_max: Optional[float] = None
    critical_min: Optional[float] = None
    critical_max: Optional[float] = None
    patient_name: Optional[str] = None
    class Config:
        from_attributes = True

# Instrument schemas
class InstrumentCreate(BaseModel):
    instrument_code: str
    instrument_name: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    location: Optional[str] = None
    serial_number: Optional[str] = None

class InstrumentUpdate(BaseModel):
    instrument_name: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class InstrumentResponse(BaseModel):
    id: int
    instrument_code: str
    instrument_name: str
    manufacturer: Optional[str]
    model: Optional[str]
    location: Optional[str]
    serial_number: Optional[str]
    status: str
    last_calibration: Optional[datetime]
    next_calibration: Optional[datetime]
    created_at: datetime
    class Config:
        from_attributes = True

# Dashboard
class DashboardStats(BaseModel):
    total_patients: int
    total_samples_today: int
    pending_results: int
    completed_today: int
    total_tests: int
    total_instruments: int


# Test Panel schemas
class TestPanelItemResponse(BaseModel):
    id: int
    test_id: int
    test_name: Optional[str] = None
    test_code: Optional[str] = None
    unit: Optional[str] = None
    class Config:
        from_attributes = True

class TestPanelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    test_ids: List[int] = []

class TestPanelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    test_ids: Optional[List[int]] = None

class TestPanelResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    test_count: Optional[int] = 0
    items: Optional[List[TestPanelItemResponse]] = []
    created_at: datetime
    class Config:
        from_attributes = True

# Invoice schemas
class InvoiceItemCreate(BaseModel):
    description: str
    test_id: Optional[int] = None
    amount: float

class InvoiceCreate(BaseModel):
    patient_id: int
    sample_id: Optional[int] = None
    items: List[InvoiceItemCreate]
    notes: Optional[str] = None

class InvoicePayment(BaseModel):
    amount: float
    notes: Optional[str] = None

class InvoiceItemResponse(BaseModel):
    id: int
    description: str
    test_id: Optional[int]
    amount: float
    class Config:
        from_attributes = True

class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    patient_id: int
    patient_name: Optional[str] = None
    sample_id: Optional[int]
    total_amount: float
    paid_amount: float
    balance: Optional[float] = None
    status: str
    notes: Optional[str]
    items: Optional[List[InvoiceItemResponse]] = []
    created_at: datetime
    class Config:
        from_attributes = True

# Reagent schemas
class ReagentCreate(BaseModel):
    name: str
    catalog_number: Optional[str] = None
    current_stock: float = 0.0
    min_stock_level: float = 0.0
    unit: Optional[str] = None
    expiry_date: Optional[datetime] = None
    supplier: Optional[str] = None
    instrument_id: Optional[int] = None
    notes: Optional[str] = None

class ReagentUpdate(BaseModel):
    name: Optional[str] = None
    catalog_number: Optional[str] = None
    current_stock: Optional[float] = None
    min_stock_level: Optional[float] = None
    unit: Optional[str] = None
    expiry_date: Optional[datetime] = None
    supplier: Optional[str] = None
    instrument_id: Optional[int] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class ReagentResponse(BaseModel):
    id: int
    name: str
    catalog_number: Optional[str]
    current_stock: float
    min_stock_level: float
    unit: Optional[str]
    expiry_date: Optional[datetime]
    supplier: Optional[str]
    instrument_id: Optional[int]
    instrument_name: Optional[str] = None
    notes: Optional[str]
    is_active: bool
    low_stock: Optional[bool] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Audit Log schemas
class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    username: Optional[str] = None
    action: str
    table_name: Optional[str]
    record_id: Optional[int]
    old_value: Optional[str]
    new_value: Optional[str]
    ip_address: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# Patient history
class PatientHistoryEntry(BaseModel):
    id: int
    sample_id: str
    sample_type: str
    collection_date: datetime
    status: str
    priority: Optional[str] = "routine"
    test_count: int = 0
    result_count: int = 0
    has_critical: bool = False
    class Config:
        from_attributes = True


# Reference range schemas
class ReferenceRangeCreate(BaseModel):
    gender: str = "Any"   # "M", "F", "Any"
    min_age: int = 0
    max_age: int = 999
    ref_min: Optional[float] = None
    ref_max: Optional[float] = None
    critical_min: Optional[float] = None
    critical_max: Optional[float] = None

class ReferenceRangeResponse(BaseModel):
    id: int
    test_id: int
    gender: str
    min_age: int
    max_age: int
    ref_min: Optional[float]
    ref_max: Optional[float]
    critical_min: Optional[float]
    critical_max: Optional[float]
    class Config:
        from_attributes = True


# Bulk order schemas
class BulkOrderCreate(BaseModel):
    sample_id: int
    test_ids: List[int]
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    priority: str = "normal"


# Bulk result schemas
class BulkResultItem(BaseModel):
    order_id: int
    sample_id: int
    test_id: int
    result_value: str
    unit: Optional[str] = None
    interpretation: Optional[str] = None


# Machine result input schemas
class MachineResultItem(BaseModel):
    test_code: str
    result_value: str
    unit: Optional[str] = None

class MachineResultsInput(BaseModel):
    sample_barcode: str
    results: List[MachineResultItem]
