from core.dao.employee_dao import EmployeeDAO


class NewEmployyesUseCase(object):
    def __init__(self):
        pass


    def execute(sel,employee:dict):
        try:
            new_employee = {
                'autorized': 1,
                'employees_code': employee['CodigoFuncionario'],
                'fullname': employee['NomeCompleto'],
                'rg': None,
                'cpf': None,
                'controller_code': None,
                'company_join': None,
                'remote_event_code': None,
                'remote_uuid': employee['unique'],
                'data_bloqueio_liberacao': employee['DataBloqueioLiberacao'],
                'deleted_at': None,
                'iface': 'N',
                'photo':employee['Foto'] if employee.get('Foto') not in [None, ''] else None if 'Foto' in employee else None
            }

            return EmployeeDAO.create(new_employee)

        except Exception as e:
            print(e)


        return None

