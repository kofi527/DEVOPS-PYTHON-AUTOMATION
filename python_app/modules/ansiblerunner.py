import yaml
import subprocess

class AnsibleRunner:
    def __init__(self, inventory_path):
        self.inventory_path = inventory_path

    def write_inventory(self, ips, user="gcpuser"):
        inv = {"all": {"hosts": {}}}
        for i, ip in enumerate(ips):
            inv["all"]["hosts"][f"host{i}"] = {"ansible_host": ip, "ansible_user": user}
        with open(self.inventory_path, "w") as f:
            yaml.safe_dump(inv, f)

    def run_playbook(self, playbook_path):
        subprocess.check_call(["ansible-playbook", "-i", self.inventory_path, playbook_path])
