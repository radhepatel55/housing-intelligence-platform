from azure.storage.blob import BlobServiceClient
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"

# local connection string
connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "housing-data-raw"

# Create the container if it doesn't already exist
try:
    blob_service_client.create_container(container_name)
    print(f"Created container: {container_name}")
except Exception as e:
    print(f"Container may already exist: {e}")

# Upload the interest rates file
local_file = DATA_DIR / "interest_rates_raw.csv"
blob_client = blob_service_client.get_blob_client(container=container_name, blob="interest_rates_raw.csv")

with open(local_file, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(f"Uploaded {local_file.name} to container '{container_name}'")