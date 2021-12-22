from flask import request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from extensions import db, create_app, celery, init_celery
from api.v1.user.resource import UserRegistration, UserLogin, UserLogoutAccess, UserLogoutRefresh, TokenRefresh, AllUsers, SecretResource
from api.v1.token.model import WhitelistedTokenModel
from api.v1.employee.resource import Employee
from api.v1.role.resource import Role
from api.v1.permission.resource import Permission
from api.v1.payslip.resource import Payslip
from api.v1.client.resource import Client
from api.v1.branch.resource import Branch
from api.v1.payroll_period.resource import PayrollPeriod
from api.v1.payroll_upload.resource import PayrollUpload
from api.v1.upload_file.resource import UploadFile
from api.v1.ip_log.resource import IpLog
from api.v1.ip_filter.resource import IpFilter
from api.v1.pay_element_type.resource import PayElementType
from api.v1.pay_element.resource import PayElement
from api.v1.pay_element_property.resource import PayElementProperty
from api.v1.pay_element_property_value.resource import PayElementPropertyValue
from api.v1.tk_element.resource import TkElement
from api.v1.tk_element_type.resource import TkElementType
from api.v1.tk_element_rate.resource import TkElementRate
from api.v1.task_status.resource import TaskStatus
from api.v1.employee_upload.resource import EmployeeUpload
from api.v1.recurring_upload.resource import RecurringUpload
from api.v1.loan_upload.resource import LoanUpload
from api.v1.multi_tenancy.resource import MultiTenancy
from api.v1.routine_info.resource import RoutineInfo
from api.v1.run_task.resource import RunTask
from api.v1.download_report.resource import DownloadReport
from api.v1.employee_info.resource import EmployeeInfo
from api.v1.finalize.resource import Finalize


app = create_app('config')

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_whitelist(decrypted_token):
    jti = decrypted_token['jti']
    return not WhitelistedTokenModel.is_jti_whitelisted(jti)


api = Api(app)
api.prefix = '/api'


api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/auth/token')
api.add_resource(AllUsers, '/users')
api.add_resource(Employee, '/employee')
api.add_resource(Role, '/roles', '/roles/<int:role_id>')
api.add_resource(Permission, '/permissions', '/permissions/<int:permission_id>')
api.add_resource(Payslip, '/payslips', '/payslips/<int:payslip_id>')
api.add_resource(Client, '/clients', '/clients/<int:client_id>')
api.add_resource(Branch, '/branches', '/branches/<int:branch_id>')
api.add_resource(PayrollPeriod, '/payroll-periods', '/payroll-periods/<int:payroll_period_id>')
api.add_resource(PayrollUpload, '/payroll-upload')
api.add_resource(UploadFile, '/upload-files', '/upload-files/<int:upload_file_id>')
api.add_resource(IpLog, '/ip-logs', '/ip-logs/<int:ip_log_id>')
api.add_resource(IpFilter, '/ip-filters', '/ip-filters/<int:ip_filter_id>')
api.add_resource(PayElementType, '/pay-element-types', '/pay-element-types/<int:pay_element_type_id>')
api.add_resource(PayElement, '/pay-elements', '/pay-elements/<int:pay_element_id>')
api.add_resource(PayElementProperty, '/pay-element-properties', '/pay-element-properties/<int:pay_element_property_id>')
api.add_resource(PayElementPropertyValue, '/pay-element-property-values', '/pay-element-property-values/<int:pay_element_property_value_id>')
api.add_resource(TkElement, '/tk-elements', '/tk-elements/<int:tk_element_id>')
api.add_resource(TkElementType, '/tk-element-types', '/tk-element-types/<int:tk_element_type_id>')
api.add_resource(TkElementRate, '/tk-element-rates', '/tk-element-rates/<int:tk_element_rate_id>')
api.add_resource(TaskStatus, '/task-status', '/task-status/<int:task_id>')
api.add_resource(EmployeeUpload, '/employee-upload')
api.add_resource(RecurringUpload, '/recurring-upload')
api.add_resource(LoanUpload, '/loan-upload')
api.add_resource(MultiTenancy, '/multi-tenancy', '/multi-tenancy/<string:db_name>')
api.add_resource(RoutineInfo, '/routine-infos', '/routine-infos/<string:routine_type_code>')
api.add_resource(RunTask, '/run-task')
api.add_resource(DownloadReport, '/download-report')
api.add_resource(EmployeeInfo, '/employee-infos')
api.add_resource(Finalize, '/finalize')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
