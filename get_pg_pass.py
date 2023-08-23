import os

from azure.identity import DefaultAzureCredential


def get_conn():
    azure_credential = DefaultAzureCredential()
    token = azure_credential.get_token("https://ossrdbms-aad.database.windows.net")
    return token.token