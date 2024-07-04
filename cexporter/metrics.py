from prometheus_client import Gauge

# Define the Prometheus gauge
kasm_version = Gauge('kasm_version', 'Version of the Kasm container', ['type', 'version'])
cmmc_vdi_version = Gauge('cmmc_vdi_version', 'Version of the automation code deployed from cmmc-vdi repo', ['version'])
