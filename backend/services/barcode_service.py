"""
Barcode Generation Service
"""

import os
from datetime import datetime


def generate_barcode(sample_id: str) -> str:
    """
    Generate Code128 barcode for sample
    Returns path to generated barcode image
    """
    import barcode
    from barcode.writer import ImageWriter

    barcode_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "barcodes")
    os.makedirs(barcode_dir, exist_ok=True)

    barcode_obj = barcode.get("code128", sample_id, writer=ImageWriter())
    barcode_path = os.path.join(barcode_dir, sample_id)
    barcode_obj.save(barcode_path)

    return f"{barcode_path}.png"


def generate_sample_id(lab_code: str = "ENI") -> str:
    """
    Generate unique sample ID
    Format: ENI-YYYY-HHMMSS-NNN (e.g., ENI-2026-103045-142)
    """
    import random
    now = datetime.utcnow()
    time_part = now.strftime("%H%M%S")
    rand_part = random.randint(100, 999)
    return f"{lab_code}-{now.year}-{time_part}-{rand_part}"
