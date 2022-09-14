from django.contrib import auth
from django.contrib.auth.models import User
from ninja import Router
from backend.common import response, Error
from django.contrib.sessions.models import Session
from users.api_scheam import RegisterIn,LoiginIn

router = Router(tags=["users"])


@router.post("/register", auth=None)
def user_register(request, payload: RegisterIn):
    """
    用户注册
    """
    username = payload.username
    password1 = payload.password
    password2 = payload.confirm_password

    if password1 != password2:
        return response(error=Error.PAWD_ERROR)
    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)
    user = User.objects.create_user(username=username, password=password1)
    user_info = {
        "id": user.id,
        "username": user.username
    }
    return response(item=user_info)


@router.post("/login",auth=None)
def user_login(request, payload: LoiginIn):
    """
    用户登录
    """
    username = payload.username
    password = payload.password
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active is True:
        auth.login(request, user)  # 向session表创建一条数据
        token = Session.objects.last() # 查最后一条最新的数据（数据量过多时，或者更新频率大，可能会不准确）
        user_info = {
            "id": user.id,
            "username": user.username,
            "token": token.session_key
        }
        return response(item=user_info)
    else:
        return response(error=Error.USER_OR_PAWD_ERROR)



@router.get("/bearer")
def bearer(request):
    return {"token": request.auth}
