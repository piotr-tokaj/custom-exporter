from prometheus_client import Gauge
import docker

# Define the Prometheus gauges
docker_image_count = Gauge('docker_image_count', 'Number of Docker images matching regex /atx-defense/')
docker_image_info = Gauge('docker_image_info', 'Information about Docker images on the VM', ['image'])

def collect_docker_images():
    """Function to collect data about the Docker images on the VM."""
    client = docker.from_env()
    images = client.images.list()

    docker_image_count.set(len(images))

    for image in images:
        docker_image_info.labels(image.tags[0]).set_to_current_time()

    return docker_image_count, docker_image_info
