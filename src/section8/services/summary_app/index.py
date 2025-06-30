import json
from http import HTTPStatus

import boto3
from botocore.exceptions import ClientError, BotoCoreError

AWS_REGION = 'us-east-1'

client = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def get_titan_config(text: str, points: str) -> json:
    prompt = f"""Text: {text} \n
    From the text above, summarize the story in {points} points.\n
"""
    return json.dumps(
        {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1,
            },
        }
    )


def lambda_handler(event: dict, context: dict) -> json:
    body = json.loads(event["body"])
    text = body.get("text")
    points = event["queryParameters"]["points"]

    titan_config = get_titan_config(text=text, points=points)
    try:
        if text and points:
            response = client.invoke_model(
                body=titan_config,
                modelId="amazon.titan-text-express-v1",
                accept="application/json",
                contentType="application/json"
            )
            response_body = json.loads(response.get("body").read())
            result = response_body.get("result")[0]

            return {
                "statusCode": HTTPStatus.OK,
                "body": json.dumps({
                    "summary": result.get("outputText")
                }),
            }
    except (BotoCoreError, ClientError) as error:
        print(f"[ERROR] {error}")
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({
                "error": str(error)
            }),
        }
