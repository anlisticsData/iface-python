import json
from traceback import print_tb

import core.Core
from core import Core
from core.Company import Company
from core.RemoteConnect import RemoteConnect
from core.dao.EmployeeUpdate import EmployeeUpdateAPIResponse
from core.dao.SettingsDAO import SettingsDAO
from core.constantes import __IS_DEVICE_PROCESSING__
from core.dao.employee_dao import EmployeeDAO
from core.device_dn815.UserStatusManager import UserStatusManager
from core.usecases.ByEmployeeActiveUseCase import ByEmployeeActiveUseCase
from core.usecases.ByEmployeeDesactiveUseCase import ByEmployeeDesactiveUseCase
from core.usecases.ByEmployyesUseCase import ByEmployyesUseCase
from core.usecases.NewEmployyesUseCase import NewEmployyesUseCase


class  InsertUploadUseCase(object):
    def __init__(self):
        self.cfg =  core.Core.settings()
        self.server =RemoteConnect()
        self.authenticate =  self.server.authenticate()

        if self.authenticate.get('status') == 200:
            self.company = Company(self.cfg .get('CUSTOMER', 'code'),
                              self.cfg .get('CUSTOMER', 'company'),
                              self.cfg .get('CUSTOMER', 'branch'), 0)








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
                            if "I" in employee.Operacao:

                                has_employee = EmployeeDAO.remote_employee_code(employee.CodigoFuncionario)
                                is_block = Core.is_expired(employee.DataBloqueioLiberacao)
                                if is_block==False:

                                    if has_employee is None:
                                        user_create = NewEmployyesUseCase().execute(employee)
                                        if user_create > 0:
                                            update_remote_empleyees.append(employee.unique)
                                    else:
                                        user_update = EmployeeDAO.update(has_employee['id'], has_employee)
                                        if user_update > 0:
                                            update_remote_empleyees.append(employee.unique)
                                        else:
                                            # Enviar Msn Para Bak
                                            update_remote_empleyees.append(employee.unique)

                                    manager = UserStatusManager(self.cfg.get('API', 'iface'))
                                    is_block = Core.is_expired(employee.DataBloqueioLiberacao)
                                    has_employee = EmployeeDAO.remote_employee_code(employee.CodigoFuncionario)
                                    if is_block==False  and has_employee and 'id' in has_employee:

                                        response = manager.disable_user(has_employee['id'])
                                        if response is not None:
                                            ByEmployeeDesactiveUseCase().execute(has_employee['id'])

                                    else:
                                        response = manager.enable_user(has_employee['id'])
                                        if response is not None:
                                            ByEmployeeActiveUseCase().execute(has_employee['id'], has_employee)

                if len(update_remote_empleyees) > 0:
                    response = self.server.update_employee(update_remote_empleyees)
                    if response and response.get('status') == 200:
                        print('****Adicao concluída:', response)


        except Exception as e:
            print(e)

