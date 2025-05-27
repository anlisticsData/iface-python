from core.dao.employee_dao import EmployeeDAO


class ByEmployeeDesactiveUseCase(object):
    def execute(self,employee_id:int):
        try:
            return EmployeeDAO.disabled(employee_id)
        except:
            return None