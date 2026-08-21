from azure.storage.blob import BlobServiceClient
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"

connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "housing-data-raw"

try:
    blob_service_client.create_container(container_name)
    print(f"Created container: {container_name}")
except Exception as e:
    print(f"Container may already exist: {e}")

# Upload every file
files_to_upload = ["interest_rates_raw.csv", "cmhc_rental_market_raw.csv"]

for filename in files_to_upload:
    local_file = DATA_DIR / filename
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    with open(local_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {filename}")

print("\nAll files uploaded!")