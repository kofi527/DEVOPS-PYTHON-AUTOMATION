import yaml
import requests
from pathlib import Path

PROM_CONFIG_PATH = Path(__file__).resolve().parents[2] / "monitoring" / "prometheus" / "prometheus.yml"
GRAFANA_URL = "http://localhost:3000"
GRAFANA_API_KEY = "<GRAFANA_API_KEY>"

class MonitoringManager:
    def __init__(self, prometheus_path=None):
        self.prometheus_path = Path(prometheus_path) if prometheus_path else PROM_CONFIG_PATH

    def add_prometheus_target(self, ip, port=9100):
        with open(self.prometheus_path, 'r') as f:
            cfg = yaml.safe_load(f) or {}

        scrape_jobs = cfg.setdefault('scrape_configs', [])
        node_job = None
        for j in scrape_jobs:
            if j.get('job_name') == 'node_exporter':
                node_job = j
                break
        if not node_job:
            node_job = {'job_name': 'node_exporter', 'static_configs': [{'targets': []}]}
            scrape_jobs.append(node_job)

        target = f"{ip}:{port}"
        targets = node_job['static_configs'][0].setdefault('targets', [])
        if target not in targets:
            targets.append(target)

        with open(self.prometheus_path, 'w') as f:
            yaml.safe_dump(cfg, f)

    def push_grafana_dashboard_from_file(self, dashboard_path):
        # expects a JSON dashboard file
        headers = {"Authorization": f"Bearer {GRAFANA_API_KEY}", "Content-Type": "application/json"}
        with open(dashboard_path, 'r') as f:
            dash_json = f.read()
        resp = requests.post(f"{GRAFANA_URL}/api/dashboards/db", data=dash_json, headers=headers)
        resp.raise_for_status()
        return resp.json()
