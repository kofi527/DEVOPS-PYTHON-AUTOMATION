"""Orchestrator: terraform -> ansible -> monitoring"""
import logging
from modules.terraform_runner import TerraformRunner
from modules.ansible_runner import AnsibleRunner
from modules.monitoring import MonitoringManager
from utils.logger import setup_logging
import os

setup_logging()
log = logging.getLogger(__name__)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERRAFORM_DIR = os.path.join(ROOT, "terraform", "gcp_dev")
ANSIBLE_PLAYBOOK = os.path.join(ROOT, "ansible", "playbooks", "deploy.yml")
INVENTORY_PATH = os.path.join(ROOT, "ansible", "inventories", "gcp_dev", "hosts.yml")

def main():
    tf = TerraformRunner(TERRAFORM_DIR)
    log.info("Terraform init...")
    print(tf.init())
    log.info("Terraform apply...")
    print(tf.apply(auto_approve=True))

    outputs = tf.get_outputs()
    ip = outputs.get("instance_ip")
    if not ip:
        log.error("No instance_ip found in terraform outputs: %s", outputs)
        return

    log.info("Instance IP: %s", ip)
    ans = AnsibleRunner(INVENTORY_PATH)
    ans.write_inventory([ip])
    log.info("Running Ansible playbook...")
    ans.run_playbook(ANSIBLE_PLAYBOOK)

    mm = MonitoringManager()
    mm.add_prometheus_target(ip, port=9100)
    log.info("Added Prometheus target for %s", ip)
    # optionally push dashboard
    # mm.push_grafana_dashboard_from_file(os.path.join(ROOT, "monitoring", "grafana", "dashboards", "gcp_app_dashboard.json"))

if __name__ == '__main__':
    main()
