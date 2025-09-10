import json

from firewheel.control.experiment_graph import AbstractPlugin, Vertex
from synchronic_web.network_monitor import Monitor
from synchronic_web.ledger_journal import Journal

from base_objects import Switch, VMEndpoint
from netaddr import IPNetwork


class Plugin(AbstractPlugin):
    """synchronic_web.network_monitor documentation."""

    def run(self):
        monitor = Vertex(self.g, "monitor.net")
        monitor.decorate(Monitor)

        monitor_network = IPNetwork("10.1.0.0/16")
        ips = monitor_network.iter_hosts()
        monitor_switch = Vertex(self.g)
        monitor_switch.decorate(Switch, init_args=["monitor-switch"])
        monitor_ip = next(ips)
        monitor.connect(monitor_switch, monitor_ip, monitor_network.netmask)

        journal_hosts = []

        for journal in [v for v in self.g.get_vertices() if v.is_decorated_by(Journal)]:
            index = int(journal.name.split(".", 1)[0].rsplit("-", 1)[-1])

            journal_ip = next(ips)
            journal.connect(monitor_switch, journal_ip, monitor_network.netmask)
            journal_hosts.append([journal.name, journal_ip])

            journal.drop_file(-40, "/home/ubuntu/node_exporter", "node_exporter")
            journal.run_executable(2, "/home/ubuntu/node_exporter")

        monitor.drop_content(
            -51, "/tmp/hosts", "\n".join(f"{ip} {name}" for name, ip in journal_hosts)
        )
        monitor.run_executable(
            -50, "bash", '-c "cat /tmp/hosts >> /etc/hosts && rm /tmp/hosts"'
        )
        monitor.drop_content(
            -10,
            "/home/ubuntu/monitor-compose/prometheus/targets.json",
            json.dumps(
                [
                    {
                        "targets": [f"{ip}:9100"],
                        "labels": {"instance": name.rsplit(".", 1)[0]},
                    }
                    for name, ip in journal_hosts
                ],
                indent=2,
            ),
        )
