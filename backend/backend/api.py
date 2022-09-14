from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.contrib.sessions.models import Session

from users.api import router as user_router
from projects.api import router as projects_router
from cases.apis.module_api import router as module_router
from cases.apis.testcase_api import router as case_router
from tasks.apis.task_api import router as tasks_router
from tasks.apis.report_api import router as report_api


class InvalidToken(Exception):
    """
    无效token
    """
    pass


class OverdueToken(Exception):
    """
    过期的token
    """
    pass


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        """
        自定义认证token处理
        """
        try:
            # 有效时间
            # SESSION_COOKIE_AGE
            # 当前时间
            # datetime
            # session创建时间
            session = Session.objects.get(pk=token)
            print("session", session)
        except Session.DoesNotExist:
            raise InvalidToken
        else:
            return token


api = NinjaAPI(auth=GlobalAuth)


@api.exception_handler(InvalidToken)
def on_invaild_tokne(request):
    """
    无效token返回类型
    """
    return api.create_response(request, {"default": "Invalid Token supplied"}, status=401)


@api.exception_handler(OverdueToken)
def on_overdue_tokne(request):
    """
    过期的token返回类型
    """
    return api.create_response(request, {"default": "Overdue Token supplied"}, status=402)


api.add_router("/users/", user_router)
api.add_router("/projects/", projects_router)
api.add_router("/modules/", module_router)
api.add_router("/cases/", case_router)
api.add_router("/tasks/", tasks_router)
api.add_router("/reports/", report_api)
