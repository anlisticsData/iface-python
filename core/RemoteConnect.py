import requests
from configparser import ConfigParser
from typing import Optional, List

from core.Company import Company


class RemoteConnect:
    def __init__(self, config_path="config.ini"):
        config = ConfigParser()
        config.read(config_path)

        self.url_address = config.get("API", "url")
        self.email = config.get("AUTH", "email")
        self.password = config.get("AUTH", "password")
        self.logged_in_user = self.authenticate()

    def authenticate(self) -> Optional[dict]:
        url = f"{self.url_address}/authenticate"
        data = {
            "email": self.email,
            "password": self.password
        }
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro na autenticação: {e}")
            return None

    def _post(self, endpoint: str, data: dict) -> str:
        url = f"{self.url_address}{endpoint}"
        headers = {}

        jwt = self.logged_in_user.get("data", {}).get("jwt") if self.logged_in_user else None
        if jwt:
            headers["bearer-token"] = jwt

        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Erro ao fazer POST em {endpoint}: {e}")
            return ""

    def authenticate_user(self, email: str, password: str) -> str:
        data = {"email": email, "password": password}
        return self._post("/users/request-account", data)

    def register_return(self, mv) -> str:
        data = {
            "branchCompanyCustomerConstruct": mv.branchCompanyCustomerConstruct,
            "employeeCode": mv.employeeCode,
            "readding": mv.readding,
            "recordType": mv.recordType,
            "nsr": mv.nsr
        }
        return self._post("/construction/iface/register-face-moviments", data)

    def request_face_download(self, company: Company, construction_code: str) -> str:
        branch_info = f"{company.clientCode}|{company.companyCode}|{company.banchCode}|{construction_code}"
        data = {"branchCompanyCustomerConstruct": branch_info}
        return self._post("/construction/iface/request-face-update-employye", data)

    def request_face_update(self, company: Company, employee) -> str:
        branch_info = f"{company.clientCode}|{company.companyCode}|{company.banchCode}"
        data = {
            "branchCompanyCustomer": branch_info,
            "employeeCode": employee.CodigoFuncionario,
            "workCode": employee.CodigoObra
        }
        return self._post("/construction/iface/request-face-update", data)

    def request_face_registration_active(self, company: Company) -> str:
        data = {
            "clientCode": company.clientCode,
            "customerCode": company.companyCode,
            "branchCode": company.banchCode
        }
        return self._post("/construction/iface/request-face-registration-active", data)

    def request_face_remove_active_face(self, uuid: str) -> str:
        return self._post("/construction/iface/request-face-remove", {"codeUuid": uuid})

    def update_employee(self, employee_array: List[str]) -> str:
        keys = "*".join(employee_array)
        data = {"uniquekeys": keys}
        return self._post("/construction/iface/update-employee-in-lote", data)
