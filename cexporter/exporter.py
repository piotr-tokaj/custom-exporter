from prometheus_client import start_http_server, Gauge
from .docker_net import collect_docker_networks
from .docker_image import collect_docker_images
from .docker_kasm_svc import collect_kasm_services
from .docker_kasm_workload import collect_kasm_workloads
from .kasm_agent_version import collect_kasm_agent_version 
from .kasm_webapp_version import collect_kasm_webapp_version
from .cmmc_vdi_code_version import collect_cmmc_version 
import time
import datetime

def get_hostname():
    """Reads the hostname from /etc/hostname."""
    with open('/etc/hostname', 'r') as file:
        return file.read().strip()

def collect_kasm_agent_metrics():
    print(f"[{datetime.datetime.now()}] Collecting Agent metrics...")
    collect_kasm_services()
    collect_docker_networks()
    collect_docker_images()
    collect_kasm_workloads()
    collect_kasm_agent_version()

def collect_kasm_webapp_metrics():
    print(f"[{datetime.datetime.now()}] Collecting Webapp metrics...")
    collect_kasm_services()
    collect_kasm_webapp_version()

def collect_kasm_database_metrics():
    print(f"[{datetime.datetime.now()}] Collecting Database metrics...")
    collect_kasm_services()

def collect_ansible_metrics():
    print(f"[{datetime.datetime.now()}] Collecting Ansible metrics...")
    collect_cmmc_version()


if __name__ == '__main__':

    print("Starting Custom Exporter...")
    # Start the Prometheus HTTP server
    start_http_server(8000)

    # Get the hostname
    hostname = get_hostname()

    if 'ansible' in hostname:
        collect_metrics = collect_ansible_metrics
        print(f"Hostname '{hostname}' contains 'ansible'. Starting the Ansible-specific metric collection...")
    elif 'agent' in hostname:
        collect_metrics = collect_kasm_agent_metrics
        print(f"Hostname '{hostname}' contains 'agent'. Starting the Agent-specific metric collection...")
    elif 'webapp' in hostname:
        collect_metrics = collect_kasm_webapp_metrics
        print(f"Hostname '{hostname}' contains 'webapp'. Starting the Webapp-specific metric collection...")
    elif 'database' in hostname:
        collect_metrics = collect_kasm_database_metrics
        print(f"Hostname '{hostname}' contains 'database'. Starting the Database-specific metric collection...")
    else:
        print(f"Hostname '{hostname}' doesn't match any expected pattern. Not starting any custom metric collection...")
        exit(1)

    while True:
        try:
            collect_metrics()
        except Exception as e:
            print(f"Error collecting metrics: {e}")

        # Collect metrics every 30 seconds.
        time.sleep(30)
