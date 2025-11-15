# 必要なライブラリをインポート
import boto3
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Bedrock呼び出し用のAPIクライアント作成
client = boto3.client("bedrock-runtime")

# Converse API を実行
response = client.converse(
    modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0", # モデルID
    messages=[{
        "role": "user",
        "content": [{
            "text": "こんにちは"
        }]
    }],
    additionalModelRequestFields={
        "thinking": {
            "type": "enabled",
            "budget_tokens": 1024
        }
    }
)

for content in response["output"]["message"]["content"]:
    if "reasoningContent" in content:
        print("<thinking>")
        print(content["reasoningContent"]["reasoningText"]["text"])
        print("</thinking>")
    elif "text" in content:
        print(content["text"])