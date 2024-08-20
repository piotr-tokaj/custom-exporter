import docker
from .metrics import kasm_version

def collect_kasm_agent_version():
    """Function to collect the version of the Kasm agent container."""
    client = docker.from_env()
    containers = client.containers.list(filters={"name": "kasm_agent"})
    if containers:
        kasm_agent = containers[0]
        version = kasm_agent.image.tags[0].split(':')[-1]
        kasm_version.labels(type='agent', version=version).set(1)
    else:
        # If no kasm_agent container is found, set the metric to zero
        version = "unknown"
        kasm_version.labels(type='agent', version=version).set(0)
    return kasm_version
