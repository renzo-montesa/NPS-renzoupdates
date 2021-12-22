from .model import EmployeeModel

class EmployeeHelper(object):
    @classmethod
    def getEmployees(cls, obj: dict):
        results = EmployeeModel.getEmployees()
        for key in results:
            obj[key] = results[key]
