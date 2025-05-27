from core.dao.employee_dao import EmployeeDAO


class ByEmployeeActiveUseCase(object):
    def execute(self,employee_id:int):
        try:
            return EmployeeDAO.enabled(employee_id)
        except:
            return None