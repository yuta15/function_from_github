import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import azure.functions as func
from azure.mgmt.resource import ResourceManagementClient

from funcs.fetch_subscription_id import fetch_func_subscription_ids
from funcs.get_credential import get_credential


BASE_URL_PREFIX = "resource-group"
BP = func.Blueprint()

@BP.route(f"{BASE_URL_PREFIX}/list", methods=["GET"])
def list_resource_groups(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Listing resource groups")
    # Logic to list resource groups
    try:
        credential = get_credential()
        subscription_ids = fetch_func_subscription_ids(credential)
        logging.info(f"Fetched subscription IDs: {subscription_ids}")
        rgs = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future = [executor.submit(fetch_rgs_for_sub, credential, sub_id) for sub_id in subscription_ids]
            for future_result in as_completed(future):
                rgs.extend(future_result.result())
        # for sub_id in subscription_ids:
        #     rg_client = ResourceManagementClient(credential, sub_id)
        #     resource_groups = rg_client.resource_groups.list()
        #     rgs.extend([rg.as_dict() for rg in resource_groups])
        logging.info(f"Resource groups: {rgs}")
    except Exception as e:
        logging.error(f"Error listing resource groups: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)
    return func.HttpResponse(body=json.dumps(rgs), status_code=200, mimetype="application/json")


def fetch_rgs_for_sub(credential, sub_id):
    """各スレッドでサブスク内のRGを最後まで列挙して最小構造で返す"""
    client = ResourceManagementClient(credential, sub_id)
    items = []
    for rg in client.resource_groups.list():  # ここでページングを消費（=I/Oはスレッド内）
        items.append({
            "subscriptionId": sub_id,
            "id": rg.id,
            "name": rg.name,
            "location": rg.location,
            "tags": rg.tags or {}
        })
    return items