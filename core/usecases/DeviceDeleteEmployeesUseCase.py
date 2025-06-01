import json

import core
from core import Core
from core.Company import Company
from core.RemoteConnect import RemoteConnect
from core.dao.EmployeeUpdate import EmployeeUpdateAPIResponse
from core.dao.employee_dao import EmployeeDAO
from core.device_dn815.DeletedEmpleyeeSender import DeletedEmpleyeeSender
from core.device_dn815.DeletedLogSender import DeletedLogSender
from core.device_dn815.UserStatusManager import UserStatusManager
from core.usecases.ByEmployeeActiveUseCase import ByEmployeeActiveUseCase
from core.usecases.ByEmployeeDesactiveUseCase import ByEmployeeDesactiveUseCase
from core.usecases.NewEmployyesUseCase import NewEmployyesUseCase


class DeviceDeleteEmployeesUseCase(object):
    def __init__(self):
        self.cfg = core.Core.settings()
        self.server = RemoteConnect()
        self.authenticate = self.server.authenticate()

        if self.authenticate.get('status') == 200:
            self.company = Company(self.cfg.get('CUSTOMER', 'code'),
                                   self.cfg.get('CUSTOMER', 'company'),
                                   self.cfg.get('CUSTOMER', 'branch'), 0)




    def execute(self):
        try:
            update_remote_empleyees = []
            if self.authenticate.get('status') == 200:
                users = self.server.request_face_download_all(self.company, self.cfg.get('CONSTRUCTION', 'code'))
                response_users = json.loads(users) if isinstance(users, str) else users
                if response_users.get('data') is not None:
                    if response_users.get('data') is not None:
                        employees = EmployeeUpdateAPIResponse.from_json(users)
                        for employee in employees.data:
                            if "E" in employee.Operacao:

                                has_employee = EmployeeDAO.remote_employee_code(employee.CodigoFuncionario)
                                if has_employee is not None:
                                   use_case = DeletedEmpleyeeSender(self.cfg.get('API', 'iface'))
                                   response=use_case.send_deleted_employees(has_employee['id'])
                                   if response is  None:
                                       EmployeeDAO.delete_in_device(has_employee['id'])
                                       update_remote_empleyees.append(employee.unique)


                if len(update_remote_empleyees) > 0:
                    response = self.server.update_employee(update_remote_empleyees)
                    if response and response.get('status') == 200:
                        print('****Adicao concluída:', response)



        except Exception as e:
            print(e)
