import json
import boto3
import os

agent = boto3.client("bedrock-agent-runtime", region_name=os.environ.get("AWS_REGION", "ap-northeast-1"))

# ナレッジベースの住所指定
KB_ID = "PFGIPCLL9G"
MODEL_ARN = "arn:aws:bedrock:ap-northeast-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"

# 質問文をナレッジベースへ
def lambda_handler(event, context):
    body = json.loads(event["body"])
    question = body["question"]

    resp = agent.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {"knowledgeBaseId": KB_ID, "modelArn": MODEL_ARN},
        },
    )
# ナレッジベースからのjson
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"answer": resp["output"]["text"]}, ensure_ascii=False),
    }
