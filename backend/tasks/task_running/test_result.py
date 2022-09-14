import os
import unittest
import requests
from XTestRunner import XMLTestRunner
from ddt import ddt, data, file_data, idata, unpack
from xml.dom.minidom import parse
from tasks.models import TestResult

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA = os.path.join(BASE_DIR, "test_data.json")
TEST_REPORT = os.path.join(BASE_DIR, "xml_result.xml")


def save_test_result(task_id):
    """
    保存测试结果
    """
    # 打开xml文档
    dom = parse(TEST_REPORT)
    # 得到文档元素对象
    root = dom.documentElement
    testsuites = root.getElementsByTagName("testsuite")

    # 获取标签内对应的属性值
    name = testsuites[0].getAttribute("name")
    tests = testsuites[0].getAttribute("tests")
    time = testsuites[0].getAttribute("time")
    failures = testsuites[0].getAttribute("failures")
    errors = testsuites[0].getAttribute("errors")
    skipped = testsuites[0].getAttribute("skipped")
    passed = int(tests) - int(failures) - int(errors) - int(skipped)

    with open(TEST_REPORT,"r",encoding='utf-8') as f:
        result = f.read()

        TestResult.objects.create(
            task_id = task_id,
            name = name,
            passed=passed,
            error = errors,
            failure=failures,
            skipped=skipped,
            tests = tests,
            run_time=time,
            result=result
        )
