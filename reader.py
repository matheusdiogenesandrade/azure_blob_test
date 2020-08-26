import os
import time
import sys
from azure.storage.blob import BlobServiceClient
from azure.storage.common.models import LocationMode
from azure.storage.common.retry import LinearRetry

def read():
    # params 
    conn_str = os.environ['AZURE_STORAGE_CONNECTIONSTRING']
    container_name = os.environ['AZURE_CONTAINER_NAME']
    uploaded_file = "Log.txt"
    try:
        # Create a reference to the blob client and container using the storage account name and key
#        blob_client = BlockBlobService(account_name, account_key)
        blob_client = BlobServiceClient.from_connection_string(conn_str=conn_str)
    except Exception as ex:
        print("Please make sure you have put the correct storage account name and key.")
        print(ex)
    # Set the location mode to secondary, so you can check just the secondary data center.
    blob_client.location_mode = LocationMode.SECONDARY
    blob_client.retry = LinearRetry(backoff=0).retry
    # Before proceeding, wait until the blob has been replicated to the secondary data center.
    # Loop and check for the presence of the blob once in a second until it hits 60 seconds
    # or until it finds it
    counter = 0
    while counter < 60:
        counter += 1
        sys.stdout.write("\nAttempt {0} to see if the blob has replicated to the secondary storage yet.".format(counter))
        sys.stdout.flush()
        if uploaded_file in blob_client.get_container_client(container_name).list_blobs():
            break
        # Wait a second, then loop around and try again
        # When it's finished replicating to the secondary, continue.
        time.sleep(1)

if __name__ == '__main__':
    try:
        read()
    except Exception as e:
        print("Error thrown = {0}".format(e))
