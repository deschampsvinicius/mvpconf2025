import os
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    key_vault_url = os.environ.get("KEY_VAULT_URL")
    secret_name = os.environ.get("SECRET_NAME", "demo-secret")

    if not key_vault_url:
        return func.HttpResponse("KEY_VAULT_URL not set in environment.", status_code=500)

    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret = client.get_secret(secret_name)
        return func.HttpResponse(f"Secret value: {secret.value}")
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
