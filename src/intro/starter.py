import pprint
from typing import Dict

import boto3

br_client = boto3.client(service_name="bedrock", region_name="us-east-1")

pp = pprint.PrettyPrinter(depth=4)

def list_foundation_models():
    response = br_client.list_foundation_models()
    number_of_foundation_models = len(response["modelSummaries"])
    print(f"Found {number_of_foundation_models} foundation models.")
    pp.pprint(response)


def get_foundation_model(model_identifier: str) -> Dict:
    response = br_client.get_foundation_model(modelIdentifier=model_identifier)
    pp.pprint(response)
    return response


if __name__ == "__main__":
    # list_foundation_models()
    get_foundation_model("mistral.mistral-large-2402-v1:0")