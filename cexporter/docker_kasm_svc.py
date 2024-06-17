from prometheus_client import start_http_server, Gauge
import docker

# Define the gauge for KASM services
kasm_service_count = Gauge('kasm_service_count', 'Number of Kasm services')
kasm_service_status = Gauge('kasm_service_status', 'Status of Kasm services (1 for running, 0 for down)', ['container_name'])

def collect_kasm_services():
    """Function to collect the number of Kasm services and their status."""
    client = docker.from_env()
    containers = client.containers.list(all=True)

    kasm_count = 0
    for container in containers:
        if container.name.startswith('kasm_'):
            kasm_count += 1
            # Check if the container is running
            if container.status == 'running':
                kasm_service_status.labels(container.name).set(1)
            else:
                kasm_service_status.labels(container.name).set(0)

    kasm_service_count.set(kasm_count)
    return kasm_service_count, kasm_service_status
