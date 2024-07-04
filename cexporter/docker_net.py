from prometheus_client import Gauge
import docker

# Create a metric to track the number of Docker networks
docker_network_count = Gauge('docker_network_count', 'Number of Docker networks starting with "z_"')

def collect_docker_networks():
    """Function to collect the number of Docker networks starting with 'z_'."""
    client = docker.from_env()
    networks = client.networks.list()
    z_networks = [network for network in networks if network.name.startswith('z_')]
    docker_network_count.set(len(z_networks))
    return docker_network_count
