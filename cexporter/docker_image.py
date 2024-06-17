from prometheus_client import start_http_server, Gauge
import docker
import re
# Define the Prometheus gauge
docker_image_count = Gauge('docker_image_count', 'Number of Docker images matching regex /atxdefense/')

def collect_docker_images():
    """Function to collect the number of Docker images matching regex /atxdefense/."""
    client = docker.from_env()
    images = client.images.list()
    pattern = re.compile(r"atx-defense")
    matching_images = [image for image in images if any(pattern.search(tag) for tag in image.tags)]
    docker_image_count.set(len(matching_images))
    return docker_image_count
