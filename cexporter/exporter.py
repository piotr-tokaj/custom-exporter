from prometheus_client import start_http_server, Gauge
from .docker_net import collect_docker_networks
from .docker_image import collect_docker_images
from .docker_kasm_svc import collect_kasm_services 
import time

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        collect_docker_networks()
        collect_docker_images()
        collect_kasm_services()
        time.sleep(30)

