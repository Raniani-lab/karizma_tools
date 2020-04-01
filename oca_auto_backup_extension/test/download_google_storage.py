import logging
import os
import shutil
import traceback
from contextlib import contextmanager
from datetime import datetime, timedelta
from glob import iglob
from google.cloud import storage
from google.cloud import exceptions as GC_exceptions

GOOGLE_APPLICATION_CREDENTIALS = "/opt/gcloud/GCLOUD-STORAGE/KARIZMA-CLOUD-ca1aa0dd8fd1.json"
bucket_name = "kzm"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

def get_client_bucket(bucket_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    return client, bucket

def upload_blob(bucket_name, source_file_name, folder_gcp, filename_gcp):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

    destination_blob_name = os.path.join(folder_gcp, filename_gcp)
    
    storage_client, bucket = get_client_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

def download_blob(bucket_name, folder_gcp, filename_gcp, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

    source_blob_name = os.path.join(folder_gcp, filename_gcp)

    storage_client, bucket = get_client_bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )

if __name__ == '__main__':
    download_blob(bucket_name, 'CREDITINFO/CREDITINFO-CLEAN', '2020_03_31_14_50_52.dump.zip','/opt/2020_03_31_14_50_52.dump.zip')
