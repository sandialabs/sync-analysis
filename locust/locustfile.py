import random
from locust import HttpUser, task


class HelloWorldUser(HttpUser):

    @task
    def hello_world(self):
        key = f'key-{random.randint(0, 2**20)}'
        val = f'val-{random.randint(0, 2**20)}'

        print(key, val)
        self.client.post(
            '/interface',
            f'(*local* "password" (ledger-set! (test {key}) {val}))',
        )
