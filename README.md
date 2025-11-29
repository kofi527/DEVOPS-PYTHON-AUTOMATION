# DEVOPS-PYTHON-AUTOMATION

**Overview of the project**



**REQUIREMENTS.TXT**
  --
- ansible
- ansible-runner
- python-terraform
- prometheus-api-client
- grafana-api
- PyYAML
- requests
- google-auth
- pytest

**WORKFLOW**
  --

- Terraform creates GCP resources.
- Python retrieves Terraform outputs.
- Ansible configures instances and deploys the app.
- Prometheus collects metrics; Grafana visualizes them.
- Python automation orchestrates, logs, and monitors everything.

**Steps for installatin of Requirements**
  --
1. **install hombrew**

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)

2. **Then environment variables**

   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"

3. **Install terraform**

   brew tap hashicorp/tap
   brew install hashicorp/tap/terraform

   check version - Terraform -version

4.  **Install ansible**

     brew install ansible

     <img width="468" height="238" alt="image" src="https://github.com/user-attachments/assets/ca7b67ee-d0b0-42e0-b49a-dbe46a3840bf" />

     Verify the version - Ansible -version





