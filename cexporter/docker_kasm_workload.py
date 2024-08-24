from prometheus_client import Gauge
import docker

# Define the Prometheus gauge
kasm_workload_count = Gauge('kasm_workload_count', 'Number of running Kasm Workspaces')
kasm_workload_info = Gauge('kasm_workload_info', 'Information about running Kasm Workspaces', ['container_id', 'container_name', 'image', 'network'])

def collect_kasm_workloads():
    """Function to collect the number of running Docker containers with port 4901 exposed. Kasm Workspaces always expose this port."""
    client = docker.from_env()
    containers = client.containers.list(filters={'expose':'4901'})
    
    # Set the number of containers
    kasm_workload_count.set(len(containers))
    
    # Set information about each container
    for container in containers:
        network = get_container_network(container)
        kasm_workload_info.labels(container_id=container.id, container_name=container.name, image=container.image.tags[0], network=network).set_to_current_time()
    return kasm_workload_count, kasm_workload_info

def get_container_network(container):

    try:
        networks_dict = container.attrs['NetworkSettings']['Networks']
        networks = networks_dict.keys()
        if len(networks) == 0:
            print(f"Unable to find any networks for container {container.id} | {container.name}")
            return ""
        elif len(networks) > 1:
            print(f"Found more than 1 network for container {container.name}! Will report the first one to metrics. Printing all networks below")
            for network in networks:
                print(f"Container {container.name} has network {network}")

        return list(networks)[0]

    except (IndexError, ValueError):
        print(f"Something went very wrong when parsing log line: {log_line}")
        return ""
