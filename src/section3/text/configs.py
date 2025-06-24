import json
from decimal import Decimal
from typing import List

def titan_config(
        prompt: str,
        temperature: int | Decimal,
        top_p: int | Decimal,
        max_token_count: int = 4096,
        stop_sequences: List[str] = []
) -> json:
    return json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": max_token_count,
            "stopSequences": stop_sequences,
            "temperature": temperature,
            "topP": top_p
        }
    })


def llama_config(
        prompt: str,
        temperature: int | Decimal,
        max_gen_len: int = 512,
        top_p: int | Decimal = 0.9
) -> json:
    return json.dumps({
    "prompt": prompt,
    "max_gen_len": max_gen_len,
    "temperature": temperature,
    "top_p": top_p,
})


def deepseek_config(role: str, model_id: str, prompt: str, max_tokens: int = 512) -> json:
    app_json = "application/json"
    return json.dumps({
        "modelId": model_id,
        "contentType": app_json,
        "accept": app_json,
        "body": {
            "inferenceConfig": {
                "max_tokens": max_tokens
            },
            "messages": [
                {
                    "role": role,
                    "content": prompt
                }
            ]
        }
    })
