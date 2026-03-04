"""
Seed Data for Enigma LIMS Demo
Run: python seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, init_db
from models import User, Doctor, Patient, Sample, Test, Order, Result, Instrument
from utils.auth import hash_password
from datetime import datetime, timedelta
import random

def seed():
    init_db()
    db = SessionLocal()

    try:
        # Create admin user if not exists
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                full_name="System Administrator",
                email="admin@enigmalims.local",
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✅ Admin user created")

        # Check if already seeded
        if db.query(User).count() > 1:
            print("Database already seeded")
            return

        print("Seeding demo data...")

        # --- INSTRUMENTS ---
        instruments = [
            Instrument(instrument_code="HEMA-001", instrument_name="Sysmex XN-1000", manufacturer="Sysmex", model="XN-1000", location="Hematology Lab", serial_number="SN20240001", status="active"),
            Instrument(instrument_code="CHEM-001", instrument_name="Roche Cobas c311", manufacturer="Roche", model="Cobas c311", location="Biochemistry Lab", serial_number="SN20240002", status="active"),
            Instrument(instrument_code="URIN-001", instrument_name="Sysmex UF-1000", manufacturer="Sysmex", model="UF-1000", location="Urinalysis Lab", serial_number="SN20240003", status="active"),
            Instrument(instrument_code="MICRO-001", instrument_name="BD BACTEC FX", manufacturer="BD", model="BACTEC FX", location="Microbiology Lab", serial_number="SN20240004", status="active"),
        ]
        for inst in instruments:
            db.add(inst)
        db.flush()

        # --- TESTS ---
        tests_data = [
            # Hematology
            {"test_code": "CBC", "test_name": "Complete Blood Count", "unit": "cells/uL", "reference_min": None, "reference_max": None, "method": "Automated", "machine_id": instruments[0].id},
            {"test_code": "HGB", "test_name": "Hemoglobin", "unit": "g/dL", "reference_min": 12.0, "reference_max": 17.0, "critical_min": 7.0, "critical_max": 20.0, "method": "Automated", "machine_id": instruments[0].id},
            {"test_code": "WBC", "test_name": "White Blood Cell Count", "unit": "x10e3/uL", "reference_min": 4.5, "reference_max": 11.0, "critical_min": 2.0, "critical_max": 30.0, "method": "Automated", "machine_id": instruments[0].id},
            {"test_code": "PLT", "test_name": "Platelet Count", "unit": "x10e3/uL", "reference_min": 150.0, "reference_max": 400.0, "critical_min": 50.0, "critical_max": 1000.0, "method": "Automated", "machine_id": instruments[0].id},
            # Biochemistry
            {"test_code": "GLU", "test_name": "Fasting Blood Glucose", "unit": "mmol/L", "reference_min": 3.9, "reference_max": 6.1, "critical_min": 2.2, "critical_max": 22.2, "method": "Enzymatic", "machine_id": instruments[1].id},
            {"test_code": "CREAT", "test_name": "Creatinine", "unit": "umol/L", "reference_min": 53.0, "reference_max": 106.0, "critical_min": 20.0, "critical_max": 884.0, "method": "Jaffe", "machine_id": instruments[1].id},
            {"test_code": "UREA", "test_name": "Blood Urea Nitrogen", "unit": "mmol/L", "reference_min": 2.5, "reference_max": 6.7, "method": "Enzymatic", "machine_id": instruments[1].id},
            {"test_code": "ALT", "test_name": "Alanine Aminotransferase", "unit": "U/L", "reference_min": 7.0, "reference_max": 56.0, "critical_min": None, "critical_max": 500.0, "method": "Kinetic", "machine_id": instruments[1].id},
            {"test_code": "AST", "test_name": "Aspartate Aminotransferase", "unit": "U/L", "reference_min": 10.0, "reference_max": 40.0, "method": "Kinetic", "machine_id": instruments[1].id},
            {"test_code": "TSH", "test_name": "Thyroid Stimulating Hormone", "unit": "mIU/L", "reference_min": 0.4, "reference_max": 4.0, "method": "CLIA", "machine_id": instruments[1].id},
            # Urinalysis
            {"test_code": "UA", "test_name": "Urinalysis Complete", "unit": None, "reference_min": None, "reference_max": None, "method": "Dipstick + Microscopy", "machine_id": instruments[2].id},
            {"test_code": "UPCR", "test_name": "Urine Protein/Creatinine Ratio", "unit": "mg/mmol", "reference_min": None, "reference_max": 15.0, "method": "Calculated", "machine_id": instruments[2].id},
        ]
        tests = []
        for t in tests_data:
            test = Test(**t)
            db.add(test)
            tests.append(test)
        db.flush()

        # --- USERS ---
        users_data = [
            {"username": "technician1", "password": "tech123", "full_name": "Muhammad Ali", "role": "technician", "email": "mali@enigmalims.pk"},
            {"username": "supervisor1", "password": "super123", "full_name": "Dr. Fatima Shah", "role": "supervisor", "email": "fshah@enigmalims.pk"},
            {"username": "doctor1", "password": "doc123", "full_name": "Dr. Khalid Hussain", "role": "doctor", "email": "khussain@enigmalims.pk"},
        ]
        users = []
        for u in users_data:
            pw = u.pop("password")
            u["password_hash"] = hash_password(pw)
            user = User(**u, is_active=True)
            db.add(user)
            users.append(user)
        db.flush()

        # Get admin user
        admin = db.query(User).filter(User.username == "admin").first()

        # --- DOCTORS ---
        doctors_data = [
            {"name": "Dr. Khalid Hussain", "registration_number": "PMDC-12345", "phone": "+92-300-1234567", "email": "dr.khalid@kotli-hospital.pk", "clinic_name": "Kotli General Hospital"},
            {"name": "Dr. Ayesha Malik", "registration_number": "PMDC-23456", "phone": "+92-301-2345678", "email": "dr.ayesha@medicenter.pk", "clinic_name": "Al-Shifa Medical Center"},
            {"name": "Dr. Zubair Ahmed", "registration_number": "PMDC-34567", "phone": "+92-302-3456789", "email": "dr.zubair@clinic.pk", "clinic_name": "City Clinic Kotli"},
            {"name": "Dr. Nadia Rashid", "registration_number": "PMDC-45678", "phone": "+92-303-4567890", "email": "dr.nadia@hospital.pk", "clinic_name": "District Hospital Kotli"},
        ]
        doctors = []
        for d in doctors_data:
            doctor = Doctor(**d)
            db.add(doctor)
            doctors.append(doctor)
        db.flush()

        # --- PATIENTS ---
        first_names = ["Muhammad", "Ahmed", "Fatima", "Ayesha", "Zainab", "Ali", "Hassan", "Hafsa", "Amina", "Bilal", "Tariq", "Sana", "Nadia", "Imran", "Usman"]
        last_names = ["Khan", "Shah", "Mirza", "Akhtar", "Hussain", "Malik", "Qureshi", "Butt", "Chaudhry", "Raza"]

        patients = []
        for i in range(20):
            patient = Patient(
                name=f"{random.choice(first_names)} {random.choice(last_names)}",
                age=random.randint(15, 75),
                gender=random.choice(["Male", "Female"]),
                phone=f"+92-30{random.randint(0,9)}-{random.randint(1000000, 9999999)}",
                doctor_id=random.choice(doctors).id
            )
            db.add(patient)
            patients.append(patient)
        db.flush()

        # --- SAMPLES ---
        sample_types = ["Blood", "Urine", "Serum", "Plasma", "CSF"]
        statuses = ["pending", "testing", "completed", "approved"]
        status_weights = [0.2, 0.2, 0.4, 0.2]

        samples = []
        for i in range(30):
            days_ago = random.randint(0, 14)
            coll_date = datetime.utcnow() - timedelta(days=days_ago)
            sample = Sample(
                sample_id=f"ENI-{datetime.utcnow().year}-{10001 + i:05d}",
                patient_id=random.choice(patients).id,
                sample_type=random.choice(sample_types),
                collection_date=coll_date,
                collection_time=coll_date.strftime("%H:%M"),
                received_date=coll_date + timedelta(minutes=30),
                status=random.choices(statuses, weights=status_weights)[0]
            )
            db.add(sample)
            samples.append(sample)
        db.flush()

        # --- ORDERS & RESULTS ---
        result_statuses = ["normal", "abnormal", "critical"]
        result_weights = [0.7, 0.2, 0.1]

        for sample in samples[:25]:  # Create orders for most samples
            num_tests = random.randint(1, 4)
            selected_tests = random.sample(tests, min(num_tests, len(tests)))

            for test in selected_tests:
                doctor = random.choice(doctors)
                order = Order(
                    sample_id=sample.id,
                    test_id=test.id,
                    doctor_id=doctor.id,
                    priority=random.choices(["normal", "urgent", "stat"], weights=[0.7, 0.2, 0.1])[0],
                    status="completed" if sample.status in ["completed", "approved"] else "pending"
                )
                db.add(order)
                db.flush()

                # Add result if sample is completed/approved
                if sample.status in ["completed", "approved"]:
                    result_status = random.choices(result_statuses, weights=result_weights)[0]

                    # Generate realistic result value
                    if test.reference_min and test.reference_max:
                        if result_status == "normal":
                            val = round(random.uniform(test.reference_min, test.reference_max), 2)
                        elif result_status == "abnormal":
                            if random.random() > 0.5:
                                val = round(test.reference_max * random.uniform(1.1, 1.5), 2)
                            else:
                                val = round(test.reference_min * random.uniform(0.5, 0.9), 2)
                        else:  # critical
                            val = round(test.reference_max * random.uniform(1.6, 2.5), 2)
                        result_value = str(val)
                    else:
                        result_value = "Normal"

                    result = Result(
                        order_id=order.id,
                        sample_id=sample.id,
                        test_id=test.id,
                        result_value=result_value,
                        unit=test.unit,
                        status=result_status,
                        qc_passed=True,
                        entered_by=admin.id if admin else None,
                        entered_date=sample.received_date + timedelta(hours=random.randint(1, 8)),
                        approved_by=admin.id if sample.status == "approved" and admin else None,
                        approved_date=sample.received_date + timedelta(hours=random.randint(8, 24)) if sample.status == "approved" else None,
                        machine_generated=random.random() > 0.5
                    )
                    db.add(result)

        db.commit()
        print("Demo data seeded successfully!")
        print("\nDemo credentials:")
        print("  admin / admin123")
        print("  technician1 / tech123")
        print("  supervisor1 / super123")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
