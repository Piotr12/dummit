import os
from azure.keyvault.secrets import SecretClient
from azure.identity import EnvironmentCredential

class AzureSecretsManager:
    @staticmethod 
    def getSecretValueByName(key_vault_name, credential, secret_name):
        # this actually requires three extra env variables! 
        # AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
        KVUri = f"https://{key_vault_name}.vault.azure.net"
        credential = EnvironmentCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        return client.get_secret(secret_name).value