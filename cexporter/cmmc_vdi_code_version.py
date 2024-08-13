import requests
from .metrics import cmmc_vdi_version

def collect_cmmc_version():
    """Function to collect the cmmc vdi code version information from the metadata endpoint."""
    url = "http://169.254.169.254/computeMetadata/v1/project/attributes/code_version"
    headers = {"Metadata-Flavor": "Google"}

    print("Running cmmc vdi version collection module")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        version = response.text.strip()
        cmmc_vdi_version.labels(version=version).set(1)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cmmc vdi code version: {e}")
        version = "unknown"
        cmmc_vdi_version.labels(version=version).set(0)
    return cmmc_vdi_version
