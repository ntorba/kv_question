import random
from locust import HttpUser, task, constant_pacing

IDs = []
with open("data.txt", "r") as f:
    data = f.readlines()
    for line in data:
        IDs.append(line.split()[0])


class User(HttpUser):
    wait_time = constant_pacing(1)

    @task
    def send_request(self):
        _id = random.choice(IDs)
        self.client.post("/get_value", json={"key": _id})
