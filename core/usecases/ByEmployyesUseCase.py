from core.dao.employee_dao import EmployeeDAO


class ByEmployyesUseCase(object):
    def __init__(self):
        pass

    def execute(self,row:dict):
       try:
           if  row['CodigoFuncionario'] is  None:
               return None

           employee_id = row['CodigoFuncionario']
           return EmployeeDAO.remote_employee_code(employee_id)
       except Exception as e:
           return None



