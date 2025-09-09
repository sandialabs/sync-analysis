import json

from firewheel.control.experiment_graph import AbstractPlugin, Vertex
from synchronic_web.resource_monitor import Monitor
from synchronic_web.ledger_journal import Journal

from base_objects import Switch, VMEndpoint
from netaddr import IPNetwork


class Plugin(AbstractPlugin):
    """synchronic_web.social_agent plugin documentation."""

    def run(self):
        monitor = Vertex(self.g, "monitor.net")
        monitor.decorate(Monitor)

        monitor_network = IPNetwork("10.1.0.0/16")
        ips = monitor_network.iter_hosts()
        monitor_switch = Vertex(self.g)
        monitor_switch.decorate(Switch, init_args=["monitor-switch"])
        monitor_ip = next(ips)
        monitor.connect(monitor_switch, monitor_ip, monitor_network.netmask)

        journals = [v.name for v in self.g.get_vertices() if v.is_decorated_by(Journal)]

        for journal in journals:
            index = int(journal.name.split(".", 1)[0].rsplit("-", 1)[-1])

            journal_ip = next(ips)
            journal.connect(monitor_switch, journal_ip, monitor_network.netmask)

            journal.drop_content(-40, "/home/ubuntu/", "node_exporter")
            journal.run_executable(2, "/home/ubuntu/node_exporter")

        monitor = Vertex(self.g, "monitor.net")
        monitor.decorate(Monitor)
        monitor.drop_content(-12, "/tmp/hosts", "\n".join(j.name for j in journals))
        monitor.run_exectuable(
            -11, "bash", '-c "cat /tmp/hosts >> /etc/hosts && rm /tmp/hosts"'
        )
        monitor.drop_content(
            -10,
            "/home/ubuntu/targets.json",
            json.dumps(
                [
                    {
                        "targets": [f"{j.name}:9100" for j in journals],
                        "labels": {"env": "firewheel", "job": "journals"},
                    }
                ],
                indent=2,
            ),
        )
