import json
import subprocess
import os

class TerraformRunner:
    def __init__(self, path):
        self.path = os.path.abspath(path)

    def _run(self, *args):
        proc = subprocess.run(["terraform"] + list(args), cwd=self.path, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Terraform failed: {' '.join(args)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        return proc.stdout

    def init(self):
        return self._run("init", "-input=false")

    def apply(self, auto_approve=False):
        args = ["apply"]
        if auto_approve:
            args.append("-auto-approve")
        return self._run(*args)

    def get_outputs(self):
        out = self._run("output", "-json")
        data = json.loads(out)
        # flatten outputs: value is in data[name]['value']
        return {k: v.get("value") for k, v in data.items()}
