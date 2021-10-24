from abc import abstractmethod, abstractstaticmethod
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

# a limitation of current design is that all secrets for a testlibrary have to be in single 
# Secrets vault. Not a big deal. 

class SecretsSingleton:
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def configure(self,provider,location):
        if provider == "azure_keyvault":
            self.provider = AzureSecretsManager(location)
        else: 
            raise NotImplementedError(f"SecretsManager for provider {provider} is not implemented?") 
    
    def getSecretValueByName(self,secret_name):
        return self.provider.getSecretValueByName(secret_name)

class AzureSecretsManager:
    def __init__(self,key_vault_name):
        self.key_vault_name = key_vault_name

    def getSecretValueByName(self,secret_name):
        # this actually requires three extra env variables! 
        # AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
        AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID","not_set_what_a_sad_story")
        AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID","not_set_what_a_sad_story")
        AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET","not_set_what_a_sad_story")
        KVUri = f"https://{self.key_vault_name}.vault.azure.net"
        credential = ClientSecretCredential(
            tenant_id = AZURE_TENANT_ID,
            client_id = AZURE_CLIENT_ID,
            client_secret = AZURE_CLIENT_SECRET
        )
        client = SecretClient(vault_url=KVUri, credential=credential)
        return client.get_secret(secret_name).value