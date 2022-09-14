import os
import json
from typing import List
from ninja import Router, Query
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from backend.common import response, Error
from backend.pagination import CustomPagination
from cases.models import TestCase
from projects.models import Project
from tasks.apis.api_scheam import TaskIn, ResultOut,TasksListOut
from tasks.models import TestTask, TaskCaseRelevance,TestResult
from backend.settings import BASE_DIR
from tasks.task_running.task_running import Task
from cases.apis.api_scheam import ProjectIn

TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_CASE = os.path.join(BASE_DIR, "tasks", "task_running", "test_case.py")

router = Router(tags=["tasks"])


@router.get("/list", auth=None,response=List[TasksListOut])
@paginate(CustomPagination)
def get_tasks_list(request, filters: ProjectIn = Query(...)):
    """获取任务列表"""
    return TestTask.objects.filter(project_id=filters.project_id,is_delete=False).all()


@router.post("/", auth=None)
def create_tasks(request, data: TaskIn):
    """创建任务"""
    project = get_object_or_404(Project, pk=data.project)
    task = TestTask.objects.create(project=project, name=data.name, describe=data.describe)
    cases_json = json.dumps(data.cases)
    TaskCaseRelevance.objects.create(task_id=task.id, cases=cases_json)
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases_json
    return response(item=task_dict)


@router.post("/{task_id}/running", auth=None)
def running(request, task_id: int):
    """执行任务"""
    task = get_object_or_404(TestTask, pk=task_id)
    task.status = 1
    task.save()
    t = Task(task.id)
    t.run2()
    return response()


@router.get("/{task_id}/", auth=None)
def get_task_detail(request, task_id: int):
    """获取任务详情"""
    task = get_object_or_404(TestTask, pk=task_id)
    if task.is_delete is True:
        return response(error=Error.TASK_ALREADY_DELETE)
    relevance = TaskCaseRelevance.objects.get(task_id=task_id)
    task_dict = model_to_dict(task)
    task_dict["cases"] = json.loads(relevance.cases)
    return response(item=task_dict)


@router.put("/{task_id}/", auth=None)
def get_task_update(request, task_id: int, payload: TaskIn):
    """更新任务"""
    task = get_object_or_404(TestTask, id=task_id)
    task.name = payload.name
    task.describe = payload.describe
    task.save()

    relevance = TaskCaseRelevance.objects.get(task_id=task_id)
    relevance.cases = json.dumps(payload.cases)
    relevance.save()

    task_dict = model_to_dict(task)
    task_dict["cases"] = payload.cases
    return response(item=task_dict)


@router.delete("/{task_id}/", auth=None)
def get_task_delete(request, task_id: int):
    """删除任务"""
    task = get_object_or_404(TestTask, id=task_id)
    task.is_delete = True
    task.save()

    return response()


@router.get("/{task_id}/results", auth=None, response=List[ResultOut])
@paginate(CustomPagination)
def get_task_result(request, task_id: int, **kwargs):
    """
    获取任务运行的结果
    auth=None 该接口不需要认证 cases = [1,2,3]
    """
    task = get_object_or_404(TestTask, pk=task_id)
    return TestResult.objects.filter(task=task).all()