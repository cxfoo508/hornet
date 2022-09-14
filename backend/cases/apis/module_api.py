from typing import List
from backend.pagination import CustomPagination
from ninja import Router, Query
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from cases.models import TestCase
from backend.common import response, Error
from cases.models import Module
from projects.models import Project
from cases.apis.api_scheam import ModuleIn, ProjectIn,CaseOut

router = Router(tags=["module"])


@router.post("/", auth=None)
def create_module(request, data: ModuleIn):
    """创建模块"""
    project = Project.objects.filter(id=data.project_id)
    if len(project) == 0:
        return response(error=Error.PROJECT_NOT_EXIST)
    module = Module.objects.filter(name=data.name, project_id=data.project_id)
    if len(module) > 0:
        return response(error=Error.MODULE_NAME_EXIST)
    modules = Module.objects.create(**data.dict())
    return response(item=model_to_dict(modules))


@router.delete("/{module_id}/", auth=None)
def get_module_delete(request, module_id: int):
    """删除模块"""
    module = get_object_or_404(Module, id=module_id)
    module.is_delete = True
    module.save()

    return response()


def node_tree(nodes, current_node):
    """递归，获取子节点"""
    for node in nodes:
        if node["parent_id"] == current_node["id"]:
            current_node["children"].append(node)
            node_tree(nodes, node)
            print("current_node:", current_node)
    return current_node


def child_node(nodes, current_node):
    """判断有没有子节点，返回True，False"""
    for node in nodes:
        # 循环取出所有节点
        if node["parent_id"] == current_node["id"]:
            # 判断所有节点中的parent_id 是否等于当前节点的id
            print("有子节点", current_node["label"])
            return True
    return False


@router.get("/tree", auth=None)
def get_module_tree(request, filters: ProjectIn = Query(...)):
    """
    获取模块树
    filters为调用接口时传入的参数，
    """
    modules = Module.objects.filter(project_id=filters.project_id, is_delete=False)
    # 过滤出project_id等于传入的项目id，并且是否删除是false
    data_node = []

    for n in modules:
        # 这个循环把所有的数据装入一个列表里，但不做其他处理
        data_node.append({
            "id": n.id,
            "parent_id": n.parent_id,
            "label": n.name,
            "children": []
        })
    print("data_node:", data_node)

    data = []
    for n in data_node:
        # 这个循环对节点做分层
        is_child = child_node(data_node, n)
        # 调用方法判断是否存在子节点，传入所有数据集，传入当前选中节点
        if (n["parent_id"] == 0) and (is_child is False):
            # 判断当前选中节点的父节点id等于0，并且是否存在子节点为false
            # 达成条件则直接填充到data列表中
            data.append(n)
        elif (n["parent_id"] == 0) and (is_child is True):
            # 如果-parent_id！=0，并且id_child is True,会跳出判断，查询不出来数据了
            # 判断当前选中节点是否是根节点，并且存在子节点
            # 调用递归方法形成树结构，并追加到列表
            ret = node_tree(data_node, n)
            data.append(ret)
        # else:
            # data.append({"error:":"错误节点："+n})
            # return response(error=Error.MODULE_PITCH_EXIST,item={"请检查节点：":n})
    return response(item=data)


@router.get("/{module_id}/cases", auth=None, response=List[CaseOut])
@paginate(CustomPagination)
def get_case_list(request, module_id: int, **kwargs):
    """获取用例列表"""

    return TestCase.objects.filter(module_id=module_id, is_delete=False).all()
