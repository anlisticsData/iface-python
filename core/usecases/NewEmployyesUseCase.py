import traceback

import core.Core
from core.dao.employee_dao import EmployeeDAO


class NewEmployyesUseCase(object):
    def __init__(self):
        pass


    def execute(sel,employee):
        try:

            if employee.Foto is not None and employee.Foto != "":
                employee.Foto =employee.Foto
            else:
                employee.Foto = None


            new_employee = {
                'autorized': 1,
                'employees_code': employee.CodigoFuncionario,
                'fullname': employee.NomeCompleto,
                'rg': None,
                'cpf': None,
                'controller_code': None,
                'company_join': None,
                'remote_event_code': None,
                'remote_uuid': employee.unique,
                'data_bloqueio_liberacao': employee.DataBloqueioLiberacao,
                'deleted_at': None,
                'iface': 'N',
                'photo':employee.Foto
            }

            return EmployeeDAO.create(new_employee)

        except Exception as e:
            print(e)
            core.Core.register_event("NewEmployyesUseCase",traceback.format_exc())


        return 0

