import os
import time;
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, PublicAccess

def send():
    try:
        # params
        conn_str = os.environ['AZURE_STORAGE_CONNECTIONSTRING']
        container_name = os.environ['AZURE_CONTAINER_NAME']
        local_path = os.path.expanduser("./")
        local_file_name = "Log.txt"
        full_path_to_file = os.path.join(local_path, local_file_name)
        # Create the BlobServiceClient that is used to call the Blob service for the storage account
        blob_service_client = BlobServiceClient.from_connection_string(conn_str=conn_str)
        # Write text to the file.
        file = open(full_path_to_file,  'w')
        file.write(str(time.time()))
        file.close()
        # Upload the created file, use local_file_name for the blob name
        blob_client = blob_service_client.get_blob_client(
                container=container_name, blob=local_file_name)
        with open(full_path_to_file, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':
    send()
