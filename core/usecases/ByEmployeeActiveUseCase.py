import traceback

from core.dao.employee_dao import EmployeeDAO


class ByEmployeeActiveUseCase(object):
    def execute(self,employee_id:int,employee:dict):
        try:
            updated_fields = {
                'employees_code': employee['CodigoFuncionario'],
                'fullname': employee['NomeCompleto'],
                'data_bloqueio_liberacao': employee['DataBloqueioLiberacao'],
                'deleted_at': None,
                'iface': 'N',
                'photo': employee['Foto'] if employee.get('Foto') not in [None,''] else None if 'Foto' in employee else None
            }

            if EmployeeDAO.update(employee_id, updated_fields):
                return EmployeeDAO.enabled(employee_id)

            return None
        except Exception as e:
            f=traceback.print_exc()
            return None