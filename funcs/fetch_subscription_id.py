import logging

from azure.mgmt.subscription import SubscriptionClient



def fetch_func_subscription_ids(credential) -> list:
    """
    Fetches the subscription IDs for the Azure Function App.

    Returns:
        list: A list of subscription IDs.
    """
    subscription_client = SubscriptionClient(credential)
    subscription_ids = []
    try:
        subs = subscription_client.subscriptions.list()
        for sub in subs:
            subscription_ids.append(sub.subscription_id)
        print(subs)
    except Exception as e:
        logging.error(f"Error fetching subscription IDs: {e}")
        raise e
    return subscription_ids
