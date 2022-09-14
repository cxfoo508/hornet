from ninja import Schema
from typing import List, Any


class TasksListOut(Schema):
    id:int
    status:int
    name: str
    describe: str = None
    create_time: Any
    update_time: Any


class TaskIn(Schema):
    """
    任务入参
    """
    project: int
    name: str
    describe: str = None
    cases: list


class ResultOut(Schema):
    """测试报告返回"""
    id:int
    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    run_time: float
    result: str
    create_time: Any


class TaskOut(Schema):
    """项目出参"""
    id: int
    name: str
    describe: str
    image: str
    create_time: Any
