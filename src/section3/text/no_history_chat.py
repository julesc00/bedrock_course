import json

import boto3
from botocore.exceptions import ClientError


client = boto3.client("bedrock-runtime", region_name="us-east-1")


def get_configuration(prompt: str):
    return json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "stopSequences": [],
            "temperature": 0,
            "topP": 1
        }
    })


def execute_prompt():
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        try:
            response = client.invoke_model(
                body=get_configuration(user_input),
                modelId="amazon.titan-text-express-v1",
                accept="application/json",
                contentType="application/json"
            )
            response_body = json.loads(response.get("body").read())
            print(response_body.get("results")[0].get("outputText"))
        except (ClientError, Exception) as e:
            print(f"[ERROR] Error invoking model: {e}")
