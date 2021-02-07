from azureml.core import Workspace
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import configparser
import os

the_cwd = os.getcwd()

config = configparser.ConfigParser()
config.read(the_cwd + '\\episode_vii.ini')
ws = Workspace.get(name=config['azure.settings']['workspace_name'], 
                   subscription_id=config['azure.settings']['subscription_id'], 
                   resource_group=config['azure.settings']['resource_group'])
print('Workspace loaded.')
storage_connection_string = config['azure.settings']['storage_connection_string']
blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)

credential = blob_service_client.credential

container_client = None
for container in blob_service_client.list_containers():
    if container.name == '154fd9d2-2831-4ad7-a2e7-61ee7e620cab':
        container_client = blob_service_client.get_container_client(container)

print(type(container_client))

#csv_file_name = the_cwd + '\\data\\regression.csv'
#csv_file = open(csv_file_name, 'rb')
#container_client.upload_blob(name='regression.csv', data=csv_file)
#print('Upload complete.')

from azure.storage.blob import BlobProperties
download_file = the_cwd + '\\data\\regression_download.csv'
with open(download_file, "wb") as my_blob:
    download_stream = container_client.download_blob(BlobProperties(name='regression.csv'))
    my_blob.write(download_stream.readall())




    
