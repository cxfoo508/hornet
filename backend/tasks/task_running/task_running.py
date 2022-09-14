import os
import json
import threading
from cases.models import TestCase
from tasks.models import TestTask, TaskCaseRelevance
from backend.settings import BASE_DIR
from tasks.task_running.test_result import save_test_result

TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_CASE = os.path.join(BASE_DIR, "tasks", "task_running", "test_case.py")


class Task:
    def __init__(self,task_id):
        self.task_id = task_id

    def running(self,task_id):
        """运行测试用例"""
        print("1_读取测试用例")
        relevace = TaskCaseRelevance.objects.get(task_id=task_id)
        case_ids = []
        relevace_list = json.loads(relevace.cases)
        for rel in relevace_list:
            case_ids = case_ids + rel["casesId"]

        test_case = {}
        for cases in case_ids:
            try:
                case = TestCase.objects.get(pk=cases, is_delete=False)
                # ast.literal_eval 转换str为dict
                # dict_header = ast.literal_eval(case.header)
                # dict_params_body = ast.literal_eval(case.params_body)
                params_body = case.params_body.replace("\'", "\"")
                params_header = case.header.replace("\'", "\"")

                dict_params_body = json.loads(params_body)
                dict_header = json.loads(params_header)

                test_case[case.name] = {
                    "url": case.url,
                    "method": case.method,
                    "header": dict_header,
                    "params_type": case.params_type,
                    "params_body": dict_params_body,
                    "assert_type": case.assert_type,
                    "assert_text": case.assert_text
                }
            except TestCase.DoesNotExist:
                pass
        print("2_用例数据写到test_json文件")
        with open(TEST_DATA, "w") as f:
            f.write(json.dumps(test_case))

        # 执行用例
        print("3_执行用例")
        os.system(f"python {TEST_CASE}")
        # 读取测试结果
        print("4_保存测试结果")
        save_test_result(task_id)
        print("5_已执行完成")
        task = TestTask.objects.get(id = task_id)
        task.status = 2
        task.save()

    def run1(self):
        threads = []
        t = threading.Thread(target=self.running,args=(self.task_id,))
        threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def run2(self):
        threads = []
        t = threading.Thread(target=self.run1(), args=(self.task_id,))
        threads.append(t)
        for t in threads:
            t.start()


# if __name__ == '__main__':
#     t = Task(task)
#     t.run()