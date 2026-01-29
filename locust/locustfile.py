import os
import json
import random
from locust import HttpUser, task, events


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        key = f"key-{random.randint(0, 2**20)}"
        val = f"val-{random.randint(0, 2**20)}"

        request_data = {
            "function": "set!",
            "authentication": os.environ["SECRET"],
            "arguments": [[["*state*", "locust", key]], val],
        }
        response = self.client.post("", json=request_data)

        # Truncate request and response for readable logging
        req_truncated = (
            request_data[:80] + "..." if len(request_data) > 80 else request_data
        )
        resp_truncated = (
            response.text[:80] + "..." if len(response.text) > 80 else response.text
        )

        print(f"REQ: {req_truncated} | RESP: {resp_truncated}")
