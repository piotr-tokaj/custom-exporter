from prometheus_client import start_http_server, Gauge
from .docker_net import collect_docker_networks
from .docker_image import collect_docker_images
from .docker_kasm_svc import collect_kasm_services
from .docker_kasm_workload import collect_kasm_workloads
from .kasm_agent_version import collect_kasm_agent_version 
from .kasm_webapp_version import collect_kasm_webapp_version
from .cmmc_vdi_code_version import collect_cmmc_version 
import time
import socket

def get_hostname():
    """Reads the hostname from /etc/hostname."""
    with open('/etc/hostname', 'r') as file:
        return file.read().strip()

if __name__ == '__main__':
    # Start the Prometheus HTTP server
    start_http_server(8000)

    # Get the hostname
    hostname = get_hostname()

    while True:
        try:
            # Collect Kasm services metrics
            collect_kasm_services()
            collect_kasm_webapp_version()
            collect_cmmc_version()

            # Check if 'agent' is in the hostname and collect additional metrics if true
            if 'agent' in hostname:
                print(f"Hostname '{hostname}' contains 'agent'. Starting the Agent specific metric collection.")
                collect_docker_networks()
                collect_docker_images()
                collect_kasm_workloads()
                collect_kasm_agent_version()
            else:
                print(f"Hostname '{hostname}' does not contain 'agent'. Agent specific metric collection not initialized.")

        except Exception as e:
            print(f"Error collecting metrics: {e}")

        # Collect metrics every 30 seconds.
        time.sleep(30)
