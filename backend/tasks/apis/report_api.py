import os
from typing import List
from ninja import Router, Query
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from cases.apis.api_scheam import ProjectIn
from backend.common import response
from backend.pagination import CustomPagination
from tasks.apis.api_scheam import TasksListOut, ResultOut
from tasks.models import TestResult, TestTask
from backend.settings import BASE_DIR

TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_CASE = os.path.join(BASE_DIR, "tasks", "task_running", "test_case.py")

router = Router(tags=["reports"])


@router.get("/list", auth=None,response=List[ResultOut])
@paginate(CustomPagination)
def get_report_list(request, filters: ProjectIn = Query(...)):
    """获取报告列表"""
    tasks = TestTask.objects.filter(project_id=filters.project_id, is_delete=False).all()
    report_list = []
    for task in tasks:
        reports = TestResult.objects.filter(task_id=task.id).all()
        for report in reports:
            report_list.append(report)
    return report_list


@router.get("/{report_id}/", auth=None)
def report_detail(request, report_id: int):
    """
    获取任务详情
    auth=None 该接口不需要认证
    """
    result = get_object_or_404(TestResult, pk=report_id)
    return response(item=model_to_dict(result))


@router.delete("/{report_id}/", auth=None)
def delete_result(request, report_id: int):
    """删除报告"""
    result = get_object_or_404(TestResult, id=report_id)
    result.delete()
    return response()
