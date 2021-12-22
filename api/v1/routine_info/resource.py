from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.routine_info.model import RoutineInfoModel
from api.v1.user_role_permission_info.model import permission_required


GET_ROUTINE_INFO = 'get_routine_info'


class RoutineInfo(Resource):
    @jwt_required
    @permission_required(GET_ROUTINE_INFO)
    def get(self, routine_type_code=None):
        if routine_type_code:
            return RoutineInfoModel.get_all_by_filter(routine_type_code=routine_type_code)
        else:
            return RoutineInfoModel.get_all()
