from azure.identity import DefaultAzureCredential
import logging


def get_credential() -> DefaultAzureCredential:
    """
    Get the Azure credential using DefaultAzureCredential.
    
    This function initializes and returns an instance of DefaultAzureCredential,
    which is used to authenticate Azure SDK clients.
    
    Returns:
        DefaultAzureCredential: An instance of DefaultAzureCredential.
    """
    credential = DefaultAzureCredential()
    return credential