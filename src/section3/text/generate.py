import json
import pprint

import boto3
from botocore.exceptions import ClientError

from configs import (
    deepseek_config,
    llama_config,
    titan_config
)

pp = pprint.PrettyPrinter(depth=4)

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

DEEP_SEEK_MODEL = "deepseek.r1-v1:0"
LLAMA_MODEL = "meta.llama2-13b-chat-v1"
TITAN_MODEL = "amazon.titan-text-express-v1"

def generate_text():
    role = "software developer"
    prompt = "How can I become the best software developer?"
    app_json = "application/json"

    try:
        response = bedrock_client.invoke_model(
            modelId=TITAN_MODEL,
            contentType=app_json,
            accept=app_json,
            body=titan_config(prompt=prompt, temperature=0, top_p=1, max_token_count=512)
        )
        res_body = json.loads(response.get("body").read())
        pp.pprint(res_body)
        return res_body.get("results")
    except (ClientError, Exception) as e:
        print(f"[ERROR] Error invoking Titan model: {e}")
        return None


if __name__ == "__main__":
    res = generate_text()
    pp.pprint(res)
