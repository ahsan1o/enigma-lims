"""
API Client for PyQt6 Frontend
Handles all HTTP communication with FastAPI backend
"""

import requests
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from config import APP_CONFIG


class APIClient:
    """HTTP client for backend communication"""
    
    def __init__(self):
        self.base_url = APP_CONFIG["api_url"]
        self.timeout = APP_CONFIG["timeout"]
        self.token = None
        self.user = None
    
    def set_token(self, token: str):
        """Set JWT token for authentication"""
        self.token = token
    
    def get_headers(self) -> Dict:
        """Get request headers with authentication"""
        headers = {
            "Content-Type": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    # ========================================================================
    # HEALTH & INFO
    # ========================================================================
    
    def health_check(self) -> bool:
        """Check if server is running"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/health",
                timeout=self.timeout
            )
            return resp.status_code == 200
        except Exception:
            return False
    
    def get_server_info(self) -> Optional[Dict]:
        """Get server information"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/info",
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return None
    
    # ========================================================================
    # AUTHENTICATION
    # ========================================================================
    
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate user
        """
        try:
            data = {
                "username": username,
                "password": password
            }
            resp = requests.post(
                f"{self.base_url}/api/auth/login",
                json=data,
                timeout=self.timeout
            )
            if resp.status_code == 200:
                result = resp.json()
                self.token = result.get("access_token")
                self.user = result.get("user")
                return True
        except Exception as e:
            print(f"Login error: {str(e)}")
        return False
    
    def logout(self):
        """Logout user"""
        self.token = None
        self.user = None
    
    # ========================================================================
    # SAMPLES
    # ========================================================================
    
    def create_sample(self, sample_data: Dict) -> Optional[Dict]:
        """Create new sample"""
        try:
            resp = requests.post(
                f"{self.base_url}/api/samples",
                json=sample_data,
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 201:
                return resp.json()
        except Exception as e:
            print(f"Create sample error: {str(e)}")
        return None
    
    def get_samples(self, skip: int = 0, limit: int = 100) -> Optional[List[Dict]]:
        """Get list of samples"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/samples?skip={skip}&limit={limit}",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"Get samples error: {str(e)}")
        return None
    
    def get_sample(self, sample_id: int) -> Optional[Dict]:
        """Get sample by ID"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/samples/{sample_id}",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"Get sample error: {str(e)}")
        return None
    
    def generate_barcode(self, sample_id: str) -> Optional[str]:
        """Generate barcode for sample"""
        try:
            resp = requests.post(
                f"{self.base_url}/api/samples/{sample_id}/barcode",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json().get("barcode_path")
        except Exception as e:
            print(f"Generate barcode error: {str(e)}")
        return None
    
    # ========================================================================
    # TESTS
    # ========================================================================
    
    def get_tests(self) -> Optional[List[Dict]]:
        """Get list of available tests"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/tests",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"Get tests error: {str(e)}")
        return None
    
    # ========================================================================
    # RESULTS
    # ========================================================================
    
    def create_result(self, result_data: Dict) -> Optional[Dict]:
        """Create new result"""
        try:
            resp = requests.post(
                f"{self.base_url}/api/results",
                json=result_data,
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 201:
                return resp.json()
        except Exception as e:
            print(f"Create result error: {str(e)}")
        return None
    
    def get_results(self, sample_id: int) -> Optional[List[Dict]]:
        """Get results for sample"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/results?sample_id={sample_id}",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"Get results error: {str(e)}")
        return None
    
    def approve_result(self, result_id: int, comments: str = "") -> bool:
        """Approve result"""
        try:
            data = {"comments": comments}
            resp = requests.post(
                f"{self.base_url}/api/results/{result_id}/approve",
                json=data,
                headers=self.get_headers(),
                timeout=self.timeout
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"Approve result error: {str(e)}")
        return False
    
    # ========================================================================
    # PATIENTS
    # ========================================================================
    
    def create_patient(self, patient_data: Dict) -> Optional[Dict]:
        """Create new patient"""
        try:
            resp = requests.post(
                f"{self.base_url}/api/patients",
                json=patient_data,
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 201:
                return resp.json()
        except Exception as e:
            print(f"Create patient error: {str(e)}")
        return None
    
    def get_patients(self) -> Optional[List[Dict]]:
        """Get list of patients"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/patients",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"Get patients error: {str(e)}")
        return None
    
    # ========================================================================
    # DOCTORS
    # ========================================================================
    
    def get_doctors(self) -> Optional[List[Dict]]:
        """Get list of doctors"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/doctors",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"Get doctors error: {str(e)}")
        return None
    
    # ========================================================================
    # MACHINE INTEGRATION
    # ========================================================================
    
    def receive_machine_data(self, machine_data: Dict) -> bool:
        """Receive data from machine"""
        try:
            resp = requests.post(
                f"{self.base_url}/api/machine/results",
                json=machine_data,
                headers=self.get_headers(),
                timeout=self.timeout
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"Machine data error: {str(e)}")
        return False
    
    # ========================================================================
    # REPORTS
    # ========================================================================
    
    def generate_report(self, sample_id: int) -> Optional[bytes]:
        """Generate PDF report for sample"""
        try:
            resp = requests.get(
                f"{self.base_url}/api/reports/{sample_id}",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.content
        except Exception as e:
            print(f"Generate report error: {str(e)}")
        return None
    
    # ========================================================================
    # ERROR HANDLING
    # ========================================================================
    
    def handle_error(self, response: requests.Response) -> str:
        """Extract error message from response"""
        try:
            data = response.json()
            return data.get("detail", "Unknown error")
        except:
            return f"Error {response.status_code}: {response.text}"


# Global API client instance
api_client = APIClient()
