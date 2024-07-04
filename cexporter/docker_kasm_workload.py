from prometheus_client import Gauge
import docker
import re

# Define the Prometheus gauge
kasm_workload_count = Gauge('kasm_workload_count', 'Number of running Docker containers using "atx-defense" image')
kasm_workload_info = Gauge('kasm_workload_info', 'Information about running Docker containers using "atx-defense" image', ['container_id', 'container_name', 'image'])

def collect_kasm_workloads():
    """Function to collect the number of running Docker containers using "atx-defense" image."""
    client = docker.from_env()
    containers = client.containers.list()
    pattern = re.compile(r"atx-defense")
    matching_containers = [container for container in containers if any(pattern.search(tag) for tag in container.image.tags)]
    
    # Set the number of matching containers
    kasm_workload_count.set(len(matching_containers))
    
    # Set information about each matching container
    for container in matching_containers:
        kasm_workload_info.labels(container_id=container.id, container_name=container.name, image=container.image.tags[0]).set(1)
    return kasm_workload_count, kasm_workload_info
