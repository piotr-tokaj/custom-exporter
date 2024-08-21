from prometheus_client import Gauge
import docker

# Define the Prometheus gauge
kasm_workload_count = Gauge('kasm_workload_count', 'Number of running Kasm Workspaces')
kasm_workload_info = Gauge('kasm_workload_info', 'Information about running Kasm Workspaces', ['container_id', 'container_name', 'image'])

def collect_kasm_workloads():
    """Function to collect the number of running Docker containers with port 4901 exposed. Kasm Workspaces always expose this port."""
    client = docker.from_env()
    containers = client.containers.list(filters={'expose':'4901'})
    
    # Set the number of containers
    kasm_workload_count.set(len(containers))
    
    # Set information about each container
    for container in containers:
        kasm_workload_info.labels(container_id=container.id, container_name=container.name, image=container.image.tags[0]).set_to_current_time()
    return kasm_workload_count, kasm_workload_info
