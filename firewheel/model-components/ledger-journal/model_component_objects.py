"""This module contains all necessary Model Component Objects for synchron_web.journal."""

from firewheel.control.experiment_graph import require_class
from linux.ubuntu2204 import Ubuntu2204Server, Ubuntu2204Desktop
from utilities.tools import Utilities


@require_class(Utilities)
class Journal:

    def __init__(self, secret, periodicity, server=True):
        if server:
            self.decorate(Ubuntu2204Server)
        else:
            self.decorate(Ubuntu2204Desktop)

        self.secret = secret
        self.periodicity = periodicity
        self.add_docker()
        self.run_journal()

        num_cores = 4
        num_threads = 2
        if self.vm['vcpu']['cores'] < num_cores:
            self.vm['vcpu']['cores'] = num_cores
        if self.vm['vcpu']['threads'] < num_threads:
            self.vm['vcpu']['threads'] = num_threads
        self.vm['mem'] = 2**13

    def run_journal(self):
        env = ' '.join([
            'PORT=80',
            f'SECRET={self.secret}',
            f'PERIODICITY={self.periodicity}',
            'WINDOW=128',
        ])

        self.drop_file(-32, '/home/ubuntu/ledger-images.tar', 'ledger-images.tar')
        self.drop_file(-32, '/home/ubuntu/ledger-compose.tar', 'ledger-compose.tar')
        self.run_executable(-31, 'bash', arguments='-c "cd /home/ubuntu && tar -xf ledger-images.tar"')
        self.run_executable(-31, 'bash', arguments='-c "cd /home/ubuntu && tar -xf ledger-compose.tar"')
        self.run_executable(-30, 'bash', '-c "cd /home/ubuntu/ledger-images && for f in *; do docker load -i \\$f; done"')
        self.run_executable(1, 'bash', arguments=f'-c "cd /home/ubuntu/ledger-compose && {env} docker compose up"')
