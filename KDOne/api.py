import json
import requests
from KDOne.utils.encryption import decrypt_payload, encrypt_payload, random_key
from KDOne.models.complex import Complex
from KDOne.models.device import Device, DeviceType
from typing import Optional, List, Dict, Any


class KDOneAPI:
    BASE_URL: str = "https://ilps.naviensmartcontrol.com:3000"

    def __init__(self, username: str, password: str, base_url: str = BASE_URL) -> None:
        self.username: str = username
        self.password: str = password
        self.complex_id: Optional[str] = None
        self.base_url: str = base_url
        self.app_certify: Optional[str] = None
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

    def _send_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        request_key: str = random_key()
        payload: str = encrypt_payload(request_key, json.dumps(data))

        print(payload)
        headers: Dict[str, str] = {
            "Content-Type": "text/plain",
            "User-Agent": "homenet/10 CFNetwork/1568.200.51 Darwin/24.1.0",
            "x-message-id": request_key,
        }
        response = requests.post(
            f"{self.base_url}{endpoint}", headers=headers, data=payload
        )

        if response.status_code == 200:
            response_key: Optional[str] = response.headers.get("x-message-id")
            decrypted_data: str = decrypt_payload(response_key, response.text)
            response_data: Dict[str, Any] = json.loads(decrypted_data)

            error_code: str = response_data.get("Error_Cd", "")
            error_name: str = response_data.get("Error_Nm", "")

            if error_code != "0000" or error_name != "성공":
                raise ValueError(f"Error {error_code}: {error_name}")

            return response_data
        else:
            response.raise_for_status()

    @staticmethod
    def get_complexes() -> List[Complex]:
        response = requests.post(f"{KDOneAPI.BASE_URL}/info/complex-list")

        if response.status_code == 200:
            response_data: Dict[str, Any] = response.json()

            error_code: str = response_data.get("Error_Cd", "")
            error_name: str = response_data.get("Error_Nm", "")

            if error_code != "0000" or error_name != "성공":
                raise ValueError(f"Error {error_code}: {error_name}")

            complex_data: List[Dict[str, Any]] = response_data.get("Resources", [])
            return [Complex.from_dict(item) for item in complex_data]
        else:
            response.raise_for_status()

    def login(self, complex_id: str) -> Dict[str, Any]:
        self.complex_id = complex_id
        data: Dict[str, str] = {
            "App_Certify": "",
            "User_Id": self.username,
            "Complex": self.complex_id,
            "User_Pw": self.password,
            "App_Type": "1",
        }
        return self._send_request("/users/login2", data)

    def get_certification_code(self) -> Dict[str, Any]:
        if not self.complex_id:
            raise ValueError(
                "Complex ID not set. Call login() first or pass complex_id."
            )

        data: Dict[str, str] = {"Complex": self.complex_id, "User_Id": self.username}
        return self._send_request("/users/certification-code", data)

    def certify(self, certify_number: str) -> Dict[str, Any]:
        if not self.complex_id:
            raise ValueError(
                "Complex ID not set. Call login() first or pass complex_id."
            )

        data: Dict[str, str] = {
            "User_Id": self.username,
            "Complex": self.complex_id,
            "Certify_Number": certify_number,
        }
        response_data = self._send_request("/users/certify", data)

        # Save the App_Certify value after certification
        self.app_certify = certify_number
        return response_data

    def get_token(self) -> Dict[str, Any]:
        if not self.complex_id:
            raise ValueError(
                "Complex ID not set. Call login() first or pass complex_id."
            )

        if not self.app_certify:
            raise ValueError(
                "App certification code not available. Call certify() first."
            )

        data: Dict[str, str] = {
            "App_Certify": self.app_certify,  # Use stored App_Certify
            "User_Id": self.username,
            "User_Pw": self.password,
            "App_Type": "1",
            "Complex": self.complex_id,
        }
        response_data = self._send_request("/users/login2", data)

        # Extract and save access_token and refresh_token
        oauth_data = response_data.get("Resources", [{}])[0].get("Oauth", {})
        self.access_token = oauth_data.get("Access_Token")
        self.refresh_token = oauth_data.get("Refresh_Token")

        return response_data

    def call_elevator(self) -> Dict[str, Any]:
        if not self.access_token:
            raise ValueError("Access token not set. Call get_token() first.")

        data: Dict[str, str] = {
            "Complex": self.complex_id,
            "Access_Token": self.access_token,
            "Refresh_Token": self.refresh_token,
        }
        return self._send_request("/device/elevator-call", data)

    def get_devices(self, device_type: DeviceType) -> List[Device]:
        if not self.access_token:
            raise ValueError("Access token not set. Call get_token() first.")

        data: Dict[str, str] = {
            "Complex": self.complex_id,
            "Device_Type": device_type.value,
            "Access_Token": self.access_token,
            "Refresh_Token": self.refresh_token,
        }

        response_data = self._send_request("/device/list", data)

        device_data: List[Dict[str, Any]] = response_data.get("Resources", [])

        return [Device.from_dict(item) for item in device_data]

    def control_device(self, device: Device, status: str) -> Dict[str, Any]:
        if not self.access_token:
            raise ValueError("Access token not set. Call get_token() first.")

        data: Dict[str, str] = {
            "Sub_Id": device.sub_id,
            "Complex": self.complex_id,
            "Device_Type": device.type.value,
            "Status_Type": device.status_type.value,
            "Group_Id": device.group_id,
            "Status": status,
            "Access_Token": self.access_token,
            "Refresh_Token": self.refresh_token,
        }
        return self._send_request("/device/control", data)
