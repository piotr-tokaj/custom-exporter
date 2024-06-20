from prometheus_client import start_http_server, Gauge
from .docker_net import collect_docker_networks
from .docker_image import collect_docker_images
from .docker_kasm_svc import collect_kasm_services 
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
        # Collect Kasm services metrics
        collect_kasm_services()

        # Check if 'agent' is in the hostname and collect additional metrics if true
        if 'agent' in hostname:
            print(f"Hostname '{hostname}' contains 'agent'. Starting the agent specific metric collection.")
            collect_docker_networks()
            collect_docker_images()
        else:
            print(f"Hostname '{hostname}' does not contain 'agent'. Agent specific metric collection not initialized.")

        # Collect metrics every 30 seconds.
        time.sleep(30)

