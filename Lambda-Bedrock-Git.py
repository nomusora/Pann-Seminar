import json
import boto3
import os

# Bedrock Agent Runtime client
agent = boto3.client(
    "bedrock-agent-runtime",
    region_name=os.environ.get("AWS_REGION", "ap-northeast-1")
)

# ★ フサペチの設定に置き換える
KB_ID = "PFGIPCLL9G"   # ← kb- を除いた10文字
MODEL_ARN = "arn:aws:bedrock:ap-northeast-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"


def lambda_handler(event, context):

    # body の取り出し（REST API / HTTP API どっちでも動くようにしてある）
    try:
        if "body" in event:
            body = event["body"]
            if isinstance(body, str):
                body = json.loads(body)
        else:
            body = event
    except Exception:
        return _res(400, {"error": "invalid JSON"})

    question = body.get("question", "")

    if not question:
        return _res(400, {"error": "question is required"})

    # Bedrock Agent Runtime: retrieve_and_generate
    try:
        resp = agent.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KB_ID,
                    "modelArn": MODEL_ARN
                }
            }
        )

        answer = resp["output"]["text"]

        return _res(200, {"answer": answer})

    except Exception as e:
        return _res(500, {"error": str(e)})


def _res(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, ensure_ascii=False)
    }
