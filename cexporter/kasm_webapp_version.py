import docker
from .metrics import kasm_version

def collect_kasm_webapp_version():
    """Function to collect the version of the Kasm webapp container."""
    client = docker.from_env()
    containers = client.containers.list(filters={"name": "kasm_api"})
    print("Running webapp version collection module")
    if containers:
        kasm_api = containers[0]
        version = kasm_api.image.tags[0].split(':')[-1]
        kasm_version.labels(type='webapp', version=version).set(1)
    else:
        # If no kasm_api container is found, set the metric to zero
        version = "unknown"
        kasm_version.labels(type='webapp', version=version).set(0)
    return kasm_version
