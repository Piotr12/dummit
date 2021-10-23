import os
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

class AzureSecretsManager:
    @staticmethod 
    def getSecretValueByName(key_vault_name, secret_name):
        # this actually requires three extra env variables! 
        # AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
        AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID","not_set_what_a_sad_story")
        AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID","not_set_what_a_sad_story")
        AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET","not_set_what_a_sad_story")
        KVUri = f"https://{key_vault_name}.vault.azure.net"
        credential = ClientSecretCredential(
            tenant_id = AZURE_TENANT_ID,
            client_id = AZURE_CLIENT_ID,
            client_secret = AZURE_CLIENT_SECRET
        )
        client = SecretClient(vault_url=KVUri, credential=credential)
        return client.get_secret(secret_name).value