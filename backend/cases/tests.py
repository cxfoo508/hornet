from django.test import TestCase

# Create your tests here.
import requests

for p in range(2):

    json = {
            "name": "三级模块"+str(p),
            "project_id": 1,
            "parent_id":5
        }

    r = requests.post("http://127.0.0.1:8000/api/cases/", json=json)
    print(r.json())
