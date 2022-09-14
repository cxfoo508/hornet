from django.forms import model_to_dict


class Error:
    """
    自定义错误码，错误信息
    """
    USER_OR_PAWD_NULL = {"10010": "用户名密码不能为空"}
    USER_OR_PAWD_ERROR = {"10011": "用户名密码错误"}
    PAWD_ERROR = {"10012": "两次密码不一致"}
    USER_EXIST = {"10013": "用户名已存在"}

    PROJECT_NAME_EXIST = {"10021": "项目名称已存在"}
    PROJECT_NOT_EXIST = {"10022": "项目不存在"}
    PROJECT_ALREADY_DELETE = {"10023": "项目已被删除"}

    FILE_TYPE_ERROR = {"10031": "文件类型错误"}
    FILE_SIZE_ERROR = {"10032": "超出文件大小"}

    MODULE_NAME_EXIST = {"10041": "模块名称已存在"}
    MODULE_NOT_EXIST = {"10042": "模块不存在"}
    MODULE_ALREADY_DELETE = {"10043": "模块已被删除"}
    MODULE_NOT_EDIT = {"10044": "更新失败，不能更改自己子节点的节点"}
    MODULE_PITCH_EXIST = {"10045":"节点数据错误，请查看"}

    CASE_MODULE_ERROR = {"10051":"请求方法错误"}
    CASE_HEADER_ERROR = {"10052":"请求header错误"}
    CASE_PARAMS_ERROR = {"10053":"请求参数类型错误"}
    CASE_ASSERT_TYPE_ISNONE = {"10054":"不存在的断言类型"}
    CASE_ALREADY_DELETE = {"10055":"case已被删除"}
    CASE_NOT_EXIST = {"10056":"case不存在"}

    TASK_ALREADY_DELETE = {"10061":"任务已被删除"}


def response(success: bool = True, error=None, item=None) -> dict:
    """
    定义统一返回格式
    """
    if error is None:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]

    if item is None:
        item = {}

    resp_data = {
        "success": success,
        "error": {
            "code": error_code,
            "msg": error_msg
        }
    }

    if isinstance(item, dict):
        resp_data["item"] = item
    elif isinstance(item, list):
        resp_data["items"] = item
    elif isinstance(item, object):
        item = model_to_dict(item)
        resp_data["item"] = item
    else:
        resp_data["item"] = {}

    return resp_data